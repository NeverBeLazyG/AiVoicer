import ctypes
import json
import os
import time
import customtkinter as ctk
import openai  # Ändern Sie den Import
from pystray import Icon as TrayIcon, Menu as TrayMenu, MenuItem as TrayMenuItem
from PIL import Image
from tkinter import messagebox
import threading
import keyboard
import sounddevice as sd
import numpy as np
import whisper
import pyperclip
import torch
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Importieren von soundfile zum Speichern von Audiodaten
import soundfile as sf

# DPI-Awareness für Windows festlegen
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception as e:
    print(f"Fehler beim Setzen der DPI-Awareness: {e}")

# Globale Variablen
fs = 16000  # Abtastrate in Hertz
icon_path_normal = "icon.ico"
icon_path_recording = "icon-rec.ico"
overlay_window = None
overlay_label = None
tray_icon = None
is_recording = False
current_recording_mode = None
tray_icon = None
icon_image = None  # Neu hinzugefügt
last_hotkey_time = 0

# Neue globale Variablen für die Aufnahme
recording_thread = None
recording_buffer = []
recording_stop_event = None

# Einmaliges Laden des Whisper-Modells
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print("Loading Whisper medium model...")
whisper_model = whisper.load_model("medium", device=device)
print("Model loaded on device:", device)

def show_recording_overlay(text="Aufzeichnung..."):
    global overlay_window, overlay_label
    if overlay_window is None:
        overlay_window = ctk.CTkToplevel(master=root)
        overlay_window.geometry("180x50")
        overlay_window.attributes("-topmost", True)
        overlay_window.overrideredirect(True)
        overlay_label = ctk.CTkLabel(
            overlay_window, text=text, font=("Lucida Console", 16, "bold"))
        overlay_label.pack(padx=10, pady=10)
        overlay_window.update_idletasks()
        screen_width = overlay_window.winfo_screenwidth()
        screen_height = overlay_window.winfo_screenheight()
        overlay_width = overlay_window.winfo_width()
        overlay_height = overlay_window.winfo_height()
        x_position = (screen_width - overlay_width) // 2
        y_position = screen_height - overlay_height - 200
        overlay_window.geometry(
            f"{overlay_width}x{overlay_height}+{x_position}+{y_position}")
    else:
        overlay_label.configure(text=text)





def hide_recording_overlay():
    global overlay_window
    if overlay_window is not None:
        overlay_window.destroy()
        overlay_window = None

def is_valid_hotkey(hotkey_str):
    try:
        handler = keyboard.add_hotkey(hotkey_str, lambda: None)
        keyboard.remove_hotkey(handler)
        return True
    except Exception as e:
        return False

def save_settings_data(api_key, transcription_hotkey, text_processing_hotkey):
    data = {
        "api_key": api_key,
        "transcription_hotkey": transcription_hotkey,
        "text_processing_hotkey": text_processing_hotkey
    }
    with open("settings.json", "w") as file:
        json.dump(data, file)

def load_settings_data():
    if os.path.exists("settings.json"):
        with open("settings.json", "r") as file:
            data = json.load(file)
            return (
                data.get("api_key", ""),
                data.get("transcription_hotkey", "ctrl+shift+f9"),
                data.get("text_processing_hotkey", "ctrl+shift+f10")
            )
    return "", "ctrl+shift+f9", "ctrl+shift+f10"

def register_hotkeys():
    global transcription_hotkey_handler, text_processing_hotkey_handler

    _, transcription_hotkey, text_processing_hotkey = load_settings_data()

    transcription_hotkey_handler = None
    text_processing_hotkey_handler = None

    try:
        transcription_hotkey_handler = keyboard.add_hotkey(transcription_hotkey, on_hotkey, args=("transcription",))
    except Exception as e:
        messagebox.showerror("Fehler", f"Ungültiger Transkriptions-Hotkey: {e}")
        transcription_hotkey_handler = None

    try:
        text_processing_hotkey_handler = keyboard.add_hotkey(text_processing_hotkey, on_hotkey, args=("text_processing",))
    except Exception as e:
        messagebox.showerror("Fehler", f"Ungültiger Text-Processing-Hotkey: {e}")
        text_processing_hotkey_handler = None

    print(f"Hotkeys registriert: Transkription ({transcription_hotkey}), Text-Processing ({text_processing_hotkey})")

def unregister_hotkeys():
    global transcription_hotkey_handler, text_processing_hotkey_handler
    if transcription_hotkey_handler is not None:
        try:
            keyboard.remove_hotkey(transcription_hotkey_handler)
        except KeyError:
            pass
        transcription_hotkey_handler = None
    if text_processing_hotkey_handler is not None:
        try:
            keyboard.remove_hotkey(text_processing_hotkey_handler)
        except KeyError:
            pass
        text_processing_hotkey_handler = None

def show_settings():
    settings_window = ctk.CTkToplevel(root)
    settings_window.title("Einstellungen")

    def save_settings():
        api_key = api_key_entry.get()
        transcription_hotkey = transcription_hotkey_entry.get()
        text_processing_hotkey = text_processing_hotkey_entry.get()

        if not api_key or not transcription_hotkey or not text_processing_hotkey:
            messagebox.showerror("Fehler", "Bitte alle Felder ausfüllen.", parent=settings_window)
            return

        if not is_valid_hotkey(transcription_hotkey):
            messagebox.showerror("Fehler", "Ungültiger Transkriptions-Hotkey.", parent=settings_window)
            return

        if not is_valid_hotkey(text_processing_hotkey):
            messagebox.showerror("Fehler", "Ungültiger Text-Processing-Hotkey.", parent=settings_window)
            return

        save_settings_data(api_key, transcription_hotkey, text_processing_hotkey)
        unregister_hotkeys()
        register_hotkeys()
        messagebox.showinfo("Einstellungen", "Einstellungen gespeichert!", parent=settings_window)
        settings_window.destroy()

    api_key_label = ctk.CTkLabel(settings_window, text="Geben Sie Ihren OpenAI API Key ein:")
    api_key_label.pack(padx=20, pady=(20, 5))

    api_key_entry = ctk.CTkEntry(settings_window, width=300)
    api_key_entry.insert(0, load_settings_data()[0])
    api_key_entry.pack(padx=20, pady=5)

    transcription_hotkey_label = ctk.CTkLabel(settings_window, text="Hotkey für Transkriptionsmodus:")
    transcription_hotkey_label.pack(padx=20, pady=(10, 5))

    transcription_hotkey_entry = ctk.CTkEntry(settings_window, width=300)
    transcription_hotkey_entry.insert(0, load_settings_data()[1])
    transcription_hotkey_entry.pack(padx=20, pady=5)

    text_processing_hotkey_label = ctk.CTkLabel(settings_window, text="Hotkey für Text-Processing-Modus:")
    text_processing_hotkey_label.pack(padx=20, pady=(10, 5))

    text_processing_hotkey_entry = ctk.CTkEntry(settings_window, width=300)
    text_processing_hotkey_entry.insert(0, load_settings_data()[2])
    text_processing_hotkey_entry.pack(padx=20, pady=5)

    save_button = ctk.CTkButton(settings_window, text="Speichern", command=save_settings)
    save_button.pack(padx=20, pady=20)

def quit_app(icon, item):
    icon.stop()
    root.quit()

def update_tray_icon():
    global tray_icon, icon_image

    icon_path = icon_path_recording if is_recording else icon_path_normal

    if tray_icon is None:
        menu = TrayMenu(
            TrayMenuItem("Einstellungen", show_settings),
            TrayMenuItem("Beenden", quit_app)
        )
        icon_image = Image.open(icon_path)
        tray_icon = TrayIcon("AIVOICER", icon_image, menu=menu)
        threading.Thread(target=tray_icon.run, daemon=True).start()
        print("Tray icon initialized.")
    else:
        # Aktualisiere nur das Icon-Bild
        tray_icon.icon = Image.open(icon_path)
        tray_icon.update_menu()

# **Angepasste Aufnahmefunktionen**

def start_recording(mode):
    global is_recording, start_time, recording_buffer, recording_thread, recording_stop_event, current_recording_mode
    is_recording = True
    start_time = time.time()
    current_recording_mode = mode
    print("Recording...")

    recording_buffer = []
    recording_stop_event = threading.Event()
    recording_thread = threading.Thread(target=record_audio, args=(recording_stop_event,))
    recording_thread.start()

    update_tray_icon()
    show_recording_overlay("Aufzeichnung...")

def record_audio(stop_event):
    global recording_buffer
    with sd.InputStream(samplerate=fs, channels=1, dtype='float32') as stream:
        while not stop_event.is_set():
            data, overflowed = stream.read(1024)
            if overflowed:
                print("Overflow occurred in recording.")
            recording_buffer.append(data.copy())

def stop_recording():
    global is_recording, start_time, recording_thread, recording_buffer, current_recording_mode
    if is_recording:
        is_recording = False
        duration = time.time() - start_time
        print(f"Recording finished after {duration:.2f} seconds.")

        recording_stop_event.set()
        recording_thread.join()

        update_tray_icon()
        show_recording_overlay("Transkription...")

        if recording_buffer:
            recording_data = np.concatenate(recording_buffer, axis=0)
            if not np.isnan(recording_data).any() and not np.isinf(recording_data).any():
                save_recording(recording_data, "recording.wav")
                transcribed_text = transcribe_audio(recording_data)
                if transcribed_text:
                    print(f"Erkannter Text: {transcribed_text}")
                    if current_recording_mode == "transcription":
                        insert_text_at_cursor(transcribed_text)
                    elif current_recording_mode == "text_processing":
                        show_main_window(transcribed_text)

        hide_recording_overlay()
        current_recording_mode = None

def save_recording(audio_data, filename):
    audio_data = np.squeeze(audio_data)
    sf.write(filename, audio_data, fs)
    print(f"Aufnahme gespeichert als {filename}")

def transcribe_audio(audio_data):
    try:
        audio_data = np.squeeze(audio_data)
        result = whisper_model.transcribe(audio_data)
        return result['text']
    except Exception as e:
        print(f"Fehler bei der Transkription: {e}")
        return None

def insert_text_at_cursor(text):
    pyperclip.copy(text)
    keyboard.send("ctrl+v")
    pyperclip.copy("")

def show_main_window(transcribed_text):
    main_window = ctk.CTkToplevel(root)
    main_window.title("AIVOICER - Text-Processing")

    mouse_x = root.winfo_pointerx()
    mouse_y = root.winfo_pointery()

    main_window.geometry(f"600x400+{mouse_x}+{mouse_y}")

    button_frame = ctk.CTkFrame(main_window)
    button_frame.pack(side="left", fill="y", padx=10, pady=10)

    buttons = [
        ("Fehlerkorrektur", "Fehlerkorrektur"),
        ("Umformulieren", "Umformulieren"),
        ("Übersetzen (Englisch)", "Übersetzen (Englisch)"),
        ("Übersetzen und Umformulieren", "Übersetzen und Umformulieren"),
        ("Zusammenfassen", "Zusammenfassen")
    ]

    for btn_text, operation in buttons:
        button = ctk.CTkButton(button_frame, text=btn_text, command=lambda op=operation: on_button_click(op, transcribed_text, main_window))
        button.pack(fill="x", pady=5)

    text_frame = ctk.CTkFrame(main_window)
    text_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    text_label = ctk.CTkLabel(text_frame, text=transcribed_text, wraplength=400, anchor="nw", justify="left")
    text_label.pack(fill="both", expand=True, anchor="nw")

def on_button_click(operation, text, window):
    original_clipboard = pyperclip.paste()
    processed_text = process_text(text, operation)
    if processed_text:
        pyperclip.copy(processed_text)
        window.withdraw()
        keyboard.send('ctrl+v')
        time.sleep(0.1)
        pyperclip.copy(original_clipboard)

def process_text(text, operation):
    try:
        api_key = load_settings_data()[0]
        if not api_key:
            messagebox.showerror("Fehler", "API Key nicht gefunden!")
            return

        # OpenAI-Client initialisieren
        client = openai.OpenAI(api_key=api_key)

        # Anweisungen für die verschiedenen Operationen
        operation_instructions = {
            "Fehlerkorrektur": "Bitte korrigiere eventuelle Fehler im folgenden Text.",
            "Umformulieren": "Bitte formuliere den folgenden Text um.", 
            "Übersetzen (Englisch)": "Bitte übersetze den folgenden Text ins Englische.",
            "Übersetzen und Umformulieren": "Bitte übersetze und formuliere den folgenden Text ins Englische um.",
            "Zusammenfassen": "Bitte fasse den folgenden Text zusammen."
        }

        # Die Anweisung zur entsprechenden Operation abrufen
        instruction = operation_instructions.get(operation, f"Bitte bearbeite den folgenden Text ({operation}).")

        # Erstellen der Chat Completion mit der neuen API-Syntax
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": instruction},
                {"role": "user", "content": text}
            ],
            max_tokens=1024,
            temperature=0.7
        )

        # Das Ergebnis des Chat-Completion-Responses extrahieren und zurückgeben
        processed_text = response.choices[0].message.content.strip()
        return processed_text

    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler bei der Textverarbeitung: {e}")
        print(f"Debug - Vollständiger Fehler: {str(e)}")
        return None

def on_hotkey(mode):
    global is_recording, last_hotkey_time
    current_time = time.time()
    if current_time - last_hotkey_time < 0.5:  # 0.5 Sekunden Verzögerung
        return
    last_hotkey_time = current_time

    if is_recording:
        stop_recording()
    else:
        start_recording(mode)

# Hauptanwendung
root = ctk.CTk()
root.overrideredirect(True)
root.withdraw()  # Verstecke das Hauptfenster

# Hotkeys initial registrieren
register_hotkeys()

# Tray-Icon in einem separaten Thread starten
update_tray_icon()

# Hauptloop starten
print("Program is running...")
root.mainloop()


