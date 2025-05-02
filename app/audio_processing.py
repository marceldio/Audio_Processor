import os
import time
import subprocess
import tempfile
from pathlib import Path
from pydub import AudioSegment
import platform
import librosa
from app.key_detector import detect_key_with_music21

def normalize_filename(filename: str) -> str:
    return filename.replace(" ", "_").replace(":", "_")

def split_audio(input_path: str, output_folder: str):
    safe_filename = Path(input_path).stem.replace(" ", "_")
    track_folder = Path(output_folder) / safe_filename
    track_folder.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as temp_dir:
        subprocess.run([
            "demucs",
            "--two-stems", "vocals",
            "-o", temp_dir,
            input_path
        ], capture_output=True, text=True, check=True)

        demucs_output_dir = Path(temp_dir) / "htdemucs" / Path(input_path).stem

        vocals_path = demucs_output_dir / "vocals.wav"
        accompaniment_path = demucs_output_dir / "no_vocals.wav"

        timeout = 20
        waited = 0
        while not vocals_path.exists() or not accompaniment_path.exists():
            time.sleep(0.5)
            waited += 0.5
            if waited > timeout:
                raise FileNotFoundError("Файлы vocals.wav или no_vocals.wav не найдены после обработки Demucs.")

        vocal_output = track_folder / "vocal.mp3"
        minus_output = track_folder / "minus.mp3"

        vocal_audio = AudioSegment.from_wav(vocals_path)
        minus_audio = AudioSegment.from_wav(accompaniment_path)

        vocal_audio.export(vocal_output, format="mp3")
        minus_audio.export(minus_output, format="mp3")

        open_folder(str(track_folder))

        return vocal_output, minus_output, track_folder

def analyze_audio(file_path):
    try:
        y, sr = librosa.load(file_path, sr=22050)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        key = detect_key_with_music21(file_path)
        return tempo, key
    except Exception as e:
        print(f"[ERROR] analyze_audio failed: {e}")
        return 0, "unknown"

def open_folder(path: str):
    system_platform = platform.system()
    if system_platform == "Windows":
        os.startfile(os.path.realpath(path))
    elif system_platform == "Darwin":
        subprocess.run(["open", path])
    else:
        subprocess.run(["xdg-open", path])
