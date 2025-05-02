import librosa
import pretty_midi
import os


def extract_melody_to_midi(wav_path: str, midi_output_path: str, key: str = "concert"):
    y, sr = librosa.load(wav_path, sr=None, mono=True)
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr, fmin=80, fmax=1000)

    notes = []
    for t in range(pitches.shape[1]):
        index = magnitudes[:, t].argmax()
        pitch = pitches[index, t]
        if pitch > 0:
            midi_note = int(librosa.hz_to_midi(pitch))
            start = t * (512 / sr)
            end = start + 0.15
            notes.append((midi_note, start, end))

    # Тональность
    transpose_semitones = {
        "concert": 0,
        "eb": 3,     # Eb-инструменты (альт-саксофон)
        "bb": 2      # Bb-инструменты (тенор-саксофон)
    }.get(key.lower(), 0)

    pm = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=0)

    for note_num, start, end in notes:
        transposed = note_num + transpose_semitones
        note = pretty_midi.Note(velocity=100, pitch=transposed, start=start, end=end)
        instrument.notes.append(note)

    pm.instruments.append(instrument)
    os.makedirs(os.path.dirname(midi_output_path), exist_ok=True)
    pm.write(midi_output_path)
    return midi_output_path
