import tkinter as tk
from tkinter import filedialog, messagebox
from app.gui.localizer import Localizer

class MainWindow:
    def __init__(self, root):
        self.localizer = Localizer(language_code="en")  # стартовый язык - английский
        self.root = root
        self.root.title("Audio Processor")

        # Выбор языка интерфейса
        self.language_var = tk.StringVar(value="en")
        self.language_label = tk.Label(root, text="Language:")
        self.language_label.pack()
        self.language_option = tk.OptionMenu(
            root, self.language_var, "en", "ru", "es", "fr", "de", "it", command=self.change_language
        )
        self.language_option.pack(pady=10)

        # Кнопка выбора файла
        self.file_button = tk.Button(root, text=self.localizer.t("select_file"), command=self.select_file)
        self.file_button.pack(pady=10)

        # Выбор источника: вокал или саксофон
        self.source_var = tk.StringVar(value="vocal")
        self.source_label = tk.Label(root, text=self.localizer.t("source_label"))
        self.source_label.pack()
        self.source_option = tk.OptionMenu(
            root, self.source_var, self.localizer.t("vocal"), self.localizer.t("saxophone")
        )
        self.source_option.pack(pady=10)

        # Выбор тональности
        self.key_var = tk.StringVar(value="concert")
        self.key_label = tk.Label(root, text=self.localizer.t("key_label"))
        self.key_label.pack()
        self.key_option = tk.OptionMenu(
            root, self.key_var, self.localizer.t("concert"), self.localizer.t("eb"), self.localizer.t("bb")
        )
        self.key_option.pack(pady=10)

        # Кнопка обработки
        self.process_button = tk.Button(root, text=self.localizer.t("process"), command=self.process_audio)
        self.process_button.pack(pady=20)

    def change_language(self, language_code):
        """Изменить язык интерфейса"""
        self.localizer.load_language(language_code)
        self.refresh_labels()

    def refresh_labels(self):
        """Обновить текст всех элементов в окне после смены языка"""
        # Обновляем метки
        self.language_label.config(text=self.localizer.t("language"))
        self.file_button.config(text=self.localizer.t("select_file"))
        self.source_label.config(text=self.localizer.t("source_label"))
        self.key_label.config(text=self.localizer.t("key_label"))
        self.process_button.config(text=self.localizer.t("process"))

        # Обновляем выпадающие списки
        self.source_option["menu"].delete(0, "end")
        for key in ["vocal", "saxophone"]:
            translated = self.localizer.t(key)
            self.source_option["menu"].add_command(
                label=translated, command=lambda value=key: self.source_var.set(value)
            )

        self.key_option["menu"].delete(0, "end")
        for key in ["concert", "eb", "bb"]:
            translated = self.localizer.t(key)
            self.key_option["menu"].add_command(
                label=translated, command=lambda value=key: self.key_var.set(value)
            )

        # Сохраняем текущие внутренние значения (ключи),
        # но показываем их переведённые значения
        self.source_var.set(self.localizer.t(self.source_var.get()))
        self.key_var.set(self.localizer.t(self.key_var.get()))

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
        if file_path:
            self.selected_file = file_path
            messagebox.showinfo(
                self.localizer.t("file_selected"),
                f"{self.localizer.t('file_selected')}\n{file_path}"
            )

    def process_audio(self):
        try:
            if not hasattr(self, "selected_file"):
                messagebox.showwarning("Ошибка", self.localizer.t("error_no_file"))
                return
            messagebox.showinfo("Обработка", self.localizer.t("processing_successful"))
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
