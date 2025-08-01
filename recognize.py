import librosa
import numpy as np
from scipy.signal import correlate

def find_timecode_precise(excerpt_path, full_audio_path):
    excerpt, sr = librosa.load(excerpt_path, sr=None, mono=True)
    full, _ = librosa.load(full_audio_path, sr=sr, mono=True)

    # Extraire l'enveloppe d'énergie (rapide et robuste pour timecode)
    excerpt_env = librosa.onset.onset_strength(y=excerpt, sr=sr)
    full_env = librosa.onset.onset_strength(y=full, sr=sr)

    # Corrélation croisée
    correlation = correlate(full_env, excerpt_env, mode='valid')
    best_offset = np.argmax(correlation)

    hop_length = 512
    frame_duration = hop_length / sr
    timecode_seconds = best_offset * frame_duration

    print(f"✅ L'extrait commence vers {timecode_seconds:.2f} secondes.")
    return timecode_seconds

print(find_timecode_precise("original_2.mp3", "echantillon.mp3"))