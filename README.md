# Audio_Processor
Audio Processor — Minus &amp; Sheet Generator

📋 Краткое описание:
Программа предназначена для разделения аудиофайлов на минус (музыкальное сопровождение) и вокал с последующим извлечением нотной записи солирующей партии.
Идеально подходит для вокалистов, желающих получить минус-файл и профессионально оформленный нотный лист.

⚙️ Основной функционал:
Приём аудиофайлов формата MP3 или WAV.
Разделение аудиофайла на:
Минус (музыка без вокала).
Извлечение основной мелодии из выбранной партии.
Генерация нотного листа в формате PDF с высоким качеством оформления.
Возможность выбора тональности нот:
Concert (оригинальная тональность),
Eb (для альт-саксофона),
Bb (для тенор-саксофона).
Поддержка мультиязычного интерфейса:
Русский
Английский
Испанский
Французский
Немецкий
Итальянский
Наличие лицензионного соглашения при установке и первом запуске.
Одна бесплатная тестовая попытка обработки без лицензии.
После использования тестовой попытки требуется ввод лицензионного ключа для продолжения работы.

🛠️ Технологии и библиотеки:
Python 3.10+
Poetry для управления зависимостями
PyCharm в качестве основной IDE
Tkinter — минималистичный GUI
Demucs — разделение вокала и инструментов
Spleeter — стартовое решение для разделения
Pydub — обработка аудиофайлов
Music21 — генерация нот и преобразование в PDF
Gettext или собственные JSON локализации — мультиязычность
PyInstaller — сборка финальной версии в .exe для Windows

📂 Структура проекта:
bash
Копировать
Редактировать
audio_processor/
├── app/
│   ├── gui/
│   │   ├── main_window.py
│   │   └── localization/
│   │       ├── ru.json
│   │       ├── en.json
│   │       ├── es.json
│   │       ├── fr.json
│   │       ├── de.json
│   │       └── it.json
│   ├── audio_processing/
│   │   ├── separator.py
│   │   └── melody_extractor.py
│   ├── licensing/
│   │   ├── license_checker.py
│   │   └── license_agreement.txt
│   ├── config/
│   │   └── settings_manager.py
│   └── main.py
├── tests/
│   └── ...
├── README.md
├── pyproject.toml
└── .gitignore

📝 Полный Порядок Работы Программы:
Пользователь запускает приложение.
Выбирает язык интерфейса.
При первом запуске принимает условия лицензионного соглашения.
Выбирает:
Аудиофайл (MP3 или WAV).
Тональность нот: Concert, Eb или Bb.
Нажимает кнопку "Обработать".
Программа:
Делит аудиофайл на минус и солирующую дорожку.
Сохраняет минус в формате MP3 (minus_<оригинальное имя>.mp3).
Извлекает основную мелодию из выбранной партии.
Преобразует мелодию в ноты.
При необходимости транспонирует в нужную тональность.
Генерирует нотный лист в формате PDF (sheet_<оригинальное имя>.pdf).
Оба файла сохраняются в папку "Загрузки" пользователя.
После одной бесплатной попытки требуется ввести лицензионный ключ.

📜 Лицензионная политика:
При установке пользователь соглашается с условиями использования.
Одна бесплатная обработка без лицензии.
Для дальнейшего использования требуется ввод лицензионного ключа.
Ключи генерируются и предоставляются отдельно.

⚠️ Важные замечания:
Приоритет качества обработки выше скорости выполнения.
При наличии нескольких вокалистов/солистов программа извлекает только ведущий голос.
Поддерживаемые форматы входного аудио: MP3, WAV.
Минимальные системные требования: Windows 10, доступ к папке Загрузки.

🔥 Планы по развитию:
Поддержка дополнительных аудиоформатов (FLAC, OGG).
Возможность пакетной обработки нескольких файлов.
Расширение настроек транспонирования.

🛡️ Разработано с вниманием к качеству и удобству использования.

✅ Статус:
На этапе активной разработки.
