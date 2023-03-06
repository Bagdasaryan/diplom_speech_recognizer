import time

import pyaudio
import pyogg
import MTest
import json

# pyogg library -> https://github.com/TeamPyOgg/PyOgg/tree/master/pyogg

countOfFiles = 0

class BaseAudioStreamReceiver:
    sound = True
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    # RECORD_SECONDS = 1000
    # pAudio = pyaudio.PyAudio()

    stereoMixerName = 'Stereo Mix (Realtek(R) Audio)'
    frames = []

    indexOfStereoMixer = 2

    # stream = pAudio.open(
    #         format=FORMAT,
    #         channels=CHANNELS,
    #         rate=RATE,
    #         input=True,
    #         input_device_index=indexOfStereoMixer,
    #         frames_per_buffer=CHUNK
    #     )

    def _clearStream(self, stream, pAudio):
        stream.stop_stream()
        stream.close()
        pAudio.terminate()

    def readAudioStream(self, stream):
        for i in range(200): # 4 seconds
            data = stream.read(self.CHUNK)
            self.frames.append(data)

    def encodeToOpus(self):
        fileName = time.time()
        self.frames = []

        pAudio = pyaudio.PyAudio()
        stream = pAudio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            input_device_index=self.indexOfStereoMixer,
            frames_per_buffer=self.CHUNK
        )

        self.readAudioStream(stream)
        self._clearStream(stream, pAudio)
        pAudio.terminate()

        # filename = "result"

        # Create a OpusBufferedEncoder
        opus_buffered_encoder = pyogg.OpusBufferedEncoder()
        opus_buffered_encoder.set_application("audio")
        opus_buffered_encoder.set_sampling_frequency(48000)
        opus_buffered_encoder.set_channels(self.CHANNELS)
        opus_buffered_encoder.set_frame_size(20)  # milliseconds

        # Create an OggOpusWriter
        output_filename = "%s"%fileName + ".ogg"
        # print("Writing OggOpus file to '{:s}'".format(output_filename))
        ogg_opus_writer = pyogg.OggOpusWriter(
            output_filename,
            opus_buffered_encoder
        )

        # Encode the PCM data
        ogg_opus_writer.write(
            memoryview(bytearray(b''.join(self.frames)))
        )

        # opus_buffered_encoder = None

        # We've finished writing the file
        ogg_opus_writer.close()

        impl = SpeechToTextImpl()
        MTest.MTest().mFoo("%s" % fileName, impl)

        self.encodeToOpus()


class SpeechToTextImpl(MTest.SpeechToTextListener):
    audioStreamObject = BaseAudioStreamReceiver()

    def doAfterTextRecognition(self, recognizedText):
        recognizedObject = json.loads(recognizedText)
        print("Result: ", recognizedObject["result"])
        basr = BaseAudioStreamReceiver()
        basr.encodeToOpus()


if __name__ == "__main__":
    basr = BaseAudioStreamReceiver()
    basr.encodeToOpus()
