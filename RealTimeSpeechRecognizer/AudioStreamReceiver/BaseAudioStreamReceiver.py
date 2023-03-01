import pyaudio
import pyogg
import MTest

# pyogg library -> https://github.com/TeamPyOgg/PyOgg/tree/master/pyogg

class BaseAudioStreamReceiver:
    sound = True
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    # RECORD_SECONDS = 1000
    p = pyaudio.PyAudio()

    stereoMixerName = 'Stereo Mix (Realtek(R) Audio)'
    frames = []

    indexOfStereoMixer = 2

    stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            input_device_index=indexOfStereoMixer,
            frames_per_buffer=CHUNK
        )

    def _clearStream(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def foo(self):
        for i in range(200):
            data = self.stream.read(self.CHUNK)
            self.frames.append(data)
            # if(self.ind == 3): break

    def encodeToOpus(self):
        self.foo()
        self._clearStream()
        self.p.terminate()

        filename = "result"

        # Create a OpusBufferedEncoder
        opus_buffered_encoder = pyogg.OpusBufferedEncoder()
        opus_buffered_encoder.set_application("audio")
        opus_buffered_encoder.set_sampling_frequency(48000)
        opus_buffered_encoder.set_channels(self.CHANNELS)
        opus_buffered_encoder.set_frame_size(20)  # milliseconds

        # Create an OggOpusWriter
        output_filename = filename + ".ogg"
        print("Writing OggOpus file to '{:s}'".format(output_filename))
        ogg_opus_writer = pyogg.OggOpusWriter(
            output_filename,
            opus_buffered_encoder
        )

        # Encode the PCM data
        ogg_opus_writer.write(
            memoryview(bytearray(b''.join(self.frames)))  # FIXME
        )

        # We've finished writing the file
        ogg_opus_writer.close()

        MTest.mFoo()

BaseAudioStreamReceiver().encodeToOpus()
