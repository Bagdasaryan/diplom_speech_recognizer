import time

import pyaudio
import pyogg
import MTest
import json
import webrtcvad
import wave
from threading import Thread
from RealTimeSpeechRecognizer.VoiceDifferentiation.Differentiation import VDifferentiation

# pyogg library -> https://github.com/TeamPyOgg/PyOgg/tree/master/pyogg

countOfFiles = 0

class BaseAudioStreamReceiver:
    sound = True
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 48000 # 44100
    # RECORD_SECONDS = 1000
    # pAudio = pyaudio.PyAudio()

    stereoMixerName = 'Stereo Mix (Realtek(R) Audio)'
    frames = []

    indexOfStereoMixer = 2

    recordedFilesNames = []

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

        mIndex = 0

        previousNum = 0
        countOfRepeats = 0

        previousNumArr = []
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

                # print("No speech: ", isNoSpeech)

                if mIndex == 1:
                    previousNum = isNoSpeech

                #if isNoSpeech >= 40 and previousNum >= 40:
                if isNoSpeech >= 32 and previousNum >= 32: # (sum(previousNumArr) / len(previousNumArr)) >= 20 and len(previousNumArr) > 5:
                    countOfRepeats += 1
                else:
                    previousNum = isNoSpeech
                    countOfRepeats = 0
                    previousNumArr.append(isNoSpeech)

                if countOfRepeats > 5:
                    # print("Speak doesn't exist")
                    # TODO: call frame to ogg writer function(frames[]) and continue loop
                    thread = Thread(target=self.threadedEncodToOpus, args=(self.frames,))
                    thread.start()
                    thread.join()
                    mIndex = 0
                    # self.frames = []

    def threadedEncodToOpus(self, frameList):
        fileName = time.time()
        # Create an OggOpusWriter
        output_filename = "%s"%fileName

        # Save to wav format
        with wave.open(output_filename+".wav", "wb") as file:
            file.setnchannels(self.CHANNELS)
            file.setsampwidth(self.pAudio.get_sample_size(pyaudio.paInt16))
            file.setframerate(self.RATE)
            file.writeframes(b''.join(frameList))

        # filename = "result"

        # Create a OpusBufferedEncoder
        opus_buffered_encoder = pyogg.OpusBufferedEncoder()
        opus_buffered_encoder.set_application("audio")
        opus_buffered_encoder.set_sampling_frequency(48000)
        opus_buffered_encoder.set_channels(self.CHANNELS)
        opus_buffered_encoder.set_frame_size(20)  # milliseconds

        # print("Writing OggOpus file to '{:s}'".format(output_filename))
        ogg_opus_writer = pyogg.OggOpusWriter(
            output_filename+".ogg",
            opus_buffered_encoder
        )

        # Encode the PCM data
        ogg_opus_writer.write(
            memoryview(bytearray(b''.join(frameList)))
        )

        # opus_buffered_encoder = None

        # We've finished writing the file
        ogg_opus_writer.close()

        self.recordedFilesNames.append("%s"%fileName + ".ogg")

        self.frames = []

        differentiationThread = Thread(target=self.threadVoiceDifferentiate(), args=())
        differentiationThread.start()
        differentiationThread.join()

        # thread = Thread(target=self.threadRecognizeSpeech, args=())
        # thread.start()
        # thread.join()

    def threadVoiceDifferentiate(self):
        VDifferentiation().differentiate("%s" % self.recordedFilesNames[0])

    def threadRecognizeSpeech(self):
        impl = SpeechToTextImpl()
        MTest.MTest().mFoo("%s" % self.recordedFilesNames[0], impl)
        self.recordedFilesNames.pop(0)

    def runThreadedRecording(self):
        thread = Thread(target=self.threadedAudioStream, args=())
        thread.start()
        thread.join()


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
