import json
import os

class Localizer:
    def __init__(self, language_code="en"):
        self.language_code = language_code
        self.translations = {}
        self.load_language(language_code)

    def load_language(self, language_code):
        """Загрузить переводы из JSON-файла по коду языка."""
        try:
            path = os.path.join(os.path.dirname(__file__), "localization", f"{language_code}.json")
            with open(path, "r", encoding="utf-8") as f:
                self.translations = json.load(f)
            self.language_code = language_code
        except FileNotFoundError:
            print(f"Language file {language_code}.json not found. Falling back to English.")
            if language_code != "en":
                self.load_language("en")

    def t(self, key):
        """Вернуть перевод по ключу. Если ключа нет — вернуть сам ключ."""
        return self.translations.get(key, key)
