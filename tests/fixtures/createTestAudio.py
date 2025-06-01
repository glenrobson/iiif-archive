import numpy as np
from scipy.io.wavfile import write

filename = "tests/fixtures/assets/audio.wav"

# Audio settings
sample_rate = 44100  # 44.1 kHz
duration = 3         # seconds
frequency = 440.0    # A4 note (Hz)

# Generate time values
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# Generate a sine wave at 440 Hz
amplitude = np.iinfo(np.int16).max
waveform = (amplitude * np.sin(2 * np.pi * frequency * t)).astype(np.int16)

# Write to WAV file
write(filename, sample_rate, waveform)
print(f"WAV file saved as {filename}")
