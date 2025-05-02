from music21 import converter

def detect_key_with_music21(midi_path: str) -> str:
    try:
        score = converter.parse(midi_path)
        k = score.analyze("key")
        return f"{k.tonic.name.lower()} {k.mode.lower()}"
    except Exception as e:
        print(f"[ERROR] key detection failed: {e}")
        return "unknown"
