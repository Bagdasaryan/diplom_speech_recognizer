import webrtcvad

# Initialize a vad object
vad = webrtcvad.Vad()
# Run the VAD on 10 ms of silence and 16000 sampling rate
sample_rate = 16000
frame_duration = 30  # in ms
# Creating an audio frame of silence
frame = b'\x01\x55\x00' * int(sample_rate * frame_duration / 1000)
# Detecting speech
print(f'Contains speech: {vad.is_speech(frame, sample_rate)}')
