import time

import pyaudio
import pyogg
import MTest
import json
import webrtcvad
from threading import Thread

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

    pAudio = pyaudio.PyAudio()
    stream = pAudio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        input_device_index=indexOfStereoMixer,
        frames_per_buffer=CHUNK
    )

    def _clearStream(self, stream, pAudio):
        stream.stop_stream()
        stream.close()
        pAudio.terminate()

    def threadedAudioStream(self):
        vad = webrtcvad.Vad()
        # Run the VAD on 10 ms of silence and 16000 sampling rate
        sample_rate = 16000
        frame_duration = 10  # in ms

        isNoSpeechPrev = 0
        isNoSpeechPrevX2 = 0

        mIndex = 0
        for i in range(10000):  # 8 seconds
            data = self.stream.read(self.CHUNK)
            self.frames.append(data)

            if len(self.frames) > 1:
                mIndex += 1

            if mIndex >= 150:
                isNoSpeech = 0
                # print("Index: ", mIndex, "; Frames size: ", len(self.frames))
                for jIndex in range(len(self.frames[mIndex]) - 1):
                    oneByte = (self.frames[mIndex][jIndex]).to_bytes(2, byteorder='big')
                    frame = oneByte * int(sample_rate * frame_duration / 1000)
                    if vad.is_speech(frame, sample_rate) == False:
                        isNoSpeech += 1

                print("Is no speech: ", isNoSpeech)
                if isNoSpeech >= 15 and isNoSpeechPrev >= 10 and isNoSpeechPrevX2 >= 7:
                    print("Speak doesn't exist")
                    # TODO: call frame to ogg writer function(frames[]) and continue loop
                    thread = Thread(target=self.threadedEncodToOpus, args=(self.frames,))
                    thread.start()
                    thread.join()
                    mIndex = 0
                    self.frames = []

                    isNoSpeechPrev = 0
                    isNoSpeechPrevX2 = 0

                isNoSpeechPrev = isNoSpeech
                if mIndex % 3 == 0:
                    isNoSpeechPrevX2 = isNoSpeech

    # def readAudioStream(self, stream):
    #     vad = webrtcvad.Vad()
    #     # Run the VAD on 10 ms of silence and 16000 sampling rate
    #     sample_rate = 16000
    #     frame_duration = 10  # in ms
    #
    #     isNoSpeechPrev = 0
    #     isNoSpeechPrevX2 = 0
    #
    #     for i in range(400): # 8 seconds
    #         data = stream.read(self.CHUNK)
    #         self.frames.append(data)
    #
    #         if i >= 150:
    #             isNoSpeech = 0
    #             for jIndex in range(len(self.frames[i]) - 1):
    #                 oneByte = (self.frames[i][jIndex]).to_bytes(2, byteorder='big')
    #                 frame = oneByte * int(sample_rate * frame_duration / 1000)
    #                 if vad.is_speech(frame, sample_rate) == False:
    #                     isNoSpeech += 1
    #
    #             print("Is no speech: ", isNoSpeech)
    #             if isNoSpeech >= 15 and isNoSpeechPrev >= 10 and isNoSpeechPrevX2 >= 7:
    #                 # print("Speak doesn't exist")
    #                 break
    #             isNoSpeechPrev = isNoSpeech
    #             if i % 3 == 0:
    #                 isNoSpeechPrevX2 = isNoSpeech

    def threadedEncodToOpus(self, frameList):
        fileName = time.time()

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

    def runThreadedRecording(self):
        thread = Thread(target=self.threadedAudioStream, args=())
        thread.start()
        thread.join()

    # def encodeToOpus(self):
    #     fileName = time.time()
    #     self.frames = []
    #
    #     pAudio = pyaudio.PyAudio()
    #     stream = pAudio.open(
    #         format=self.FORMAT,
    #         channels=self.CHANNELS,
    #         rate=self.RATE,
    #         input=True,
    #         input_device_index=self.indexOfStereoMixer,
    #         frames_per_buffer=self.CHUNK
    #     )
    #
    #     self.readAudioStream(stream)
    #     self._clearStream(stream, pAudio)
    #     pAudio.terminate()
    #
    #     thread = Thread(target=self.threadedAudioStream, args=(stream,))
    #     thread.start()
    #     thread.join()
    #
    #     # filename = "result"
    #
    #     # Create a OpusBufferedEncoder
    #     opus_buffered_encoder = pyogg.OpusBufferedEncoder()
    #     opus_buffered_encoder.set_application("audio")
    #     opus_buffered_encoder.set_sampling_frequency(48000)
    #     opus_buffered_encoder.set_channels(self.CHANNELS)
    #     opus_buffered_encoder.set_frame_size(20)  # milliseconds
    #
    #     # Create an OggOpusWriter
    #     output_filename = "%s"%fileName + ".ogg"
    #     # print("Writing OggOpus file to '{:s}'".format(output_filename))
    #     ogg_opus_writer = pyogg.OggOpusWriter(
    #         output_filename,
    #         opus_buffered_encoder
    #     )
    #
    #     # Encode the PCM data
    #     ogg_opus_writer.write(
    #         memoryview(bytearray(b''.join(self.frames)))
    #     )
    #
    #     # opus_buffered_encoder = None
    #
    #     # We've finished writing the file
    #     ogg_opus_writer.close()
    #
    #     # impl = SpeechToTextImpl()
    #     # MTest.MTest().mFoo("%s" % fileName, impl)
    #
    #     self.encodeToOpus()


class SpeechToTextImpl(MTest.SpeechToTextListener):
    audioStreamObject = BaseAudioStreamReceiver()

    def doAfterTextRecognition(self, recognizedText):
        recognizedObject = json.loads(recognizedText)
        print("Result: ", recognizedObject["result"])
        # basr = BaseAudioStreamReceiver()
        # basr.encodeToOpus()


if __name__ == "__main__":
    basr = BaseAudioStreamReceiver()
    basr.runThreadedRecording()
    # basr.encodeToOpus()
