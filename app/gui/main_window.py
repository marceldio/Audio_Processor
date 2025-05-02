import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os
import platform
import subprocess
from pathlib import Path
from app.gui.localizer import Localizer
from app.audio_processing import split_audio
from tkinter import ttk
from app.melody_extractor import extract_melody_to_midi
from app.audio_processing import analyze_audio
from app.key_detector import detect_key_with_music21
import time

def open_in_musescore(midi_path, working_dir=None):
    musescore_app = "/home/md/Downloads/MuseScore-Studio-4.5.2.251141401-x86_64.AppImage"
    try:
        subprocess.Popen(
            [musescore_app, str(midi_path)],
            cwd=str(working_dir) if working_dir else None
        )
        time.sleep(5)
        result = subprocess.run(['wmctrl', '-l'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        for line in result.stdout.splitlines():
            if Path(midi_path).name in line:
                window_id = line.split()[0]
                subprocess.run(['wmctrl', '-ia', window_id])
                break
        else:
            print("[WARN] MuseScore window not found")
    except Exception as e:
        print(f"[ERROR] Could not open MuseScore: {e}")

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.selected_file = None
        self.root.title("Audio Processor")
        self.localizer = Localizer(language_code="en")

        self._init_styles()
        self._init_geometry()
        self._init_widgets()

    def _init_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure(
            "custom.Horizontal.TProgressbar",
            thickness=20,
            troughcolor="#e0e0e0",
            background="#4CAF50",
            bordercolor="#e0e0e0",
            lightcolor="#4CAF50",
            darkcolor="#4CAF50"
        )

    def _init_geometry(self):
        w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        ww, wh = w // 2, h // 2
        x, y = (w - ww) // 2, (h - wh) // 2
        self.root.geometry(f"{ww}x{wh}+{x}+{y}")

    def _init_widgets(self):
        self.language_var = tk.StringVar(value="en")
        self.language_label = tk.Label(self.root, text=self.localizer.t("language_label"))
        self.language_label.pack()

        self.language_option = tk.OptionMenu(
            self.root, self.language_var, "en", "ru", "es", "fr", "de", "it", command=self.change_language
        )
        self.language_option.pack(pady=10)

        self.file_button = tk.Button(self.root, text=self.localizer.t("select_file"), command=self.select_file)
        self.file_button.pack(pady=10)

        self.process_button = tk.Button(self.root, text=self.localizer.t("process"), command=self.process_audio)
        self.process_button.pack(pady=20)

        self.progress = ttk.Progressbar(self.root, mode="indeterminate", style="custom.Horizontal.TProgressbar")

        self.result_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.result_label.pack(pady=5)

        self.buttons_to_disable = [
            self.language_option,
            self.file_button,
            self.process_button
        ]

    def change_language(self, lang):
        self.localizer.load_language(lang)
        self.refresh_labels()

    def refresh_labels(self):
        self.language_label.config(text=self.localizer.t("language_label"))
        self.file_button.config(text=self.localizer.t("select_file"))
        self.process_button.config(text=self.localizer.t("process"))
        self.result_label.config(text="")

    def select_file(self):
        file = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
        if file:
            self.selected_file = file
            messagebox.showinfo(
                self.localizer.t("file_selected"),
                f"{self.localizer.t('file_selected')}\n{file}"
            )

    def process_audio(self):
        if not hasattr(self, "selected_file"):
            messagebox.showwarning("Ошибка", self.localizer.t("error_no_file"))
            return
        self.disable_buttons()
        self.progress.pack(pady=10)
        self.progress.start(10)
        threading.Thread(target=self._process_audio_thread, daemon=True).start()

    def _process_audio_thread(self):
        tempo = None
        key = "unknown"
        try:
            downloads = str(Path.home() / "Downloads")
            vocal_path, minus_path, folder = split_audio(self.selected_file, downloads)

            midi_path = folder / f"sheet_{Path(self.selected_file).stem}.mid"
            extract_melody_to_midi(vocal_path, str(midi_path), key="auto")

            # Открыть папку
            self.open_folder(str(folder))

            # Открыть MuseScore с рабочей директорией = folder
            open_in_musescore(midi_path, working_dir=folder)

            tempo_array = analyze_audio(self.selected_file)
            tempo = float(tempo_array[0]) if tempo_array is not None and len(tempo_array) > 0 else None

            key = detect_key_with_music21(str(midi_path))
            print(f"[DEBUG] Tempo: {tempo}, Key: {key}")

            tempo_str = f"{tempo:.1f} BPM" if tempo else "?"
            self.result_label.config(
                text=f"{self.localizer.t('detected_key')}: {key}, {self.localizer.t('detected_tempo')}: {tempo_str}"
            )

        except Exception as e:
            self.show_error(str(e))
        finally:
            self.progress.stop()
            self.progress.pack_forget()
            self.enable_buttons()
            self.root.quit()

    def show_error(self, msg):
        messagebox.showerror(self.localizer.t("error_title"), msg)

    def open_folder(self, path):
        if platform.system() == "Windows":
            os.startfile(os.path.realpath(path))
        elif platform.system() == "Darwin":
            subprocess.run(["open", path])
        else:
            subprocess.run(["xdg-open", path])

    def disable_buttons(self):
        for btn in self.buttons_to_disable:
            btn.config(state="disabled")

    def enable_buttons(self):
        for btn in self.buttons_to_disable:
            btn.config(state="normal")
