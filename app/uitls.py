import music21
import numpy as np
import io
import re
from scipy.io.wavfile import write as write_wav
from synthesizer import Synthesizer, Waveform

def note_to_frequencies(note_list):
    """Notes generated from LLM are converted to frequencies"""
    freqs = []
    
    for note_str in note_list:
        try:
            note=music21.note.Note(note_str)
            freqs.append(note.pitch.frequency)
        except: 
            continue
    
    return freqs


def generate_wav_bytes_from_notes_freq(notes_freq, rhythm=None):
    """Convert frequencies into audio, applying generated beat durations when provided."""
    
    synth = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=1.0, use_osc2=False)
    sample_rate = 44100

    beat_durations = (
        [float(value) for value in re.findall(r"\d+(?:\.\d+)?", rhythm)]
        if rhythm
        else []
    )
    audio = np.concatenate([
        synth.generate_constant_wave(
            freq,
            min(max(beat_durations[index % len(beat_durations)] * 0.5, 0.125), 2.0)
            if beat_durations
            else 0.5,
        )
        for index, freq in enumerate(notes_freq)
    ])
    
    buffer = io.BytesIO()
    write_wav(buffer, sample_rate, audio.astype(np.float32))
    
    return buffer.getvalue()