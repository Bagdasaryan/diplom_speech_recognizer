import pyaudio
import pyogg
import MTest
import webrtcvad
import wave
from threading import Thread
from RealTimeSpeechRecognizer.VoiceDifferentiation.Differentiation import VDifferentiation
from RealTimeSpeechRecognizer.VoiceDifferentiation.Differentiation import AudioTrimListener
import time

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
    recordedFilesNames = []
    # Сюда записываются параметры обрезанных файлов - [[FILE_1, USER_1], [FILE_2, USER_2], ..., [FILE_N, USER_N]]
    differentiatedAudioTrimList = []

    isVoiceDifferentiated = False
    isSpeechRecognized = True

    indexOfStereoMixer = 2
    indexOfFileForDifferentiation = 0
    indexOfRecognizedFile = 0

    # Thread type
    speechRecognitionThread = None

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

                # if mIndex == 1:
                #     previousNum = isNoSpeech

                #if isNoSpeech >= 40 and previousNum >= 40:
                if isNoSpeech >= 35 and previousNum >= 35:
                    countOfRepeats += 1
                else:
                    previousNum = isNoSpeech
                    countOfRepeats = 0
                    previousNumArr.append(isNoSpeech)

                if countOfRepeats > 1:
                    # print("Speak doesn't exist")
                    # TODO: call frame to ogg writer function(frames[]) and continue loop
                    self.threadedEncodToOpus(self.frames)
                    # self.threadOpus = Thread(target=self.threadedEncodToOpus, args=(self.frames,))
                    # self.threadOpus.start()
                    # thread.join()
                    mIndex = 0
                    # self.frames = []

    def threadedEncodToOpus(self, frameList):
        # self.frames.append(b'\x00')

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

        self.recordedFilesNames.append("%s"%fileName)

        self.frames = []

        self.isVoiceDifferentiated = True

        # if self.isVoiceDifferentiated:
        #     self.isVoiceDifferentiated = False
            # differentiationThread = Thread(target=self.threadVoiceDifferentiate(self.recordedFilesNames[self.indexOfFileForDifferentiation]), args=())
            # differentiationThread.start()

        # thread = Thread(target=self.threadRecognizeSpeech, args=())
        # thread.start()
        # thread.join()

    def threadVoiceDifferentiate(self):
        impl = DifferentiatedAudioTrimImpl()
        impl.setConstructor(self)
        while self.indexOfFileForDifferentiation < 500:
            if self.indexOfFileForDifferentiation < len(self.recordedFilesNames):
                VDifferentiation().differentiate(self.recordedFilesNames[self.indexOfFileForDifferentiation], impl)
                self.indexOfFileForDifferentiation += 1
                self.isVoiceDifferentiated = False
                # TODO: Call speech recognizing in thread
                if self.speechRecognitionThread is None or self.isSpeechRecognized:
                    print("Differentiation start")
                    self.speechRecognitionThread = Thread(target=basr.threadRecognizeSpeech, args=())
                    self.speechRecognitionThread.start()
                # elif self.speechRecognitionThread is not None and self.isSpeechRecognized == False:
                #     self.speechRecognitionThread.join()
                #     self.speechRecognitionThread = Thread(target=basr.threadRecognizeSpeech, args=())
                #     self.speechRecognitionThread.start()

    def threadRecognizeSpeech(self):
        impl = SpeechToTextImpl()
        impl.setConstructor(self)
        self.someFoo(impl)

    def someFoo(self, impl):
        if len(self.differentiatedAudioTrimList) > 0:
            if self.isSpeechRecognized:
                self.isSpeechRecognized = False
                print("Call mFoo")
                if len(self.recordedFilesNames) > 0 and self.indexOfRecognizedFile < len(self.recordedFilesNames):
                    # MTest.MTest().mFoo("%s" % self.recordedFilesNames[self.indexOfRecognizedFile], impl)
                    MTest.MTest().mFoo(self.differentiatedAudioTrimList[self.indexOfRecognizedFile], impl)
                    self.indexOfRecognizedFile += 1
                    self.recordedFilesNames.pop(0)
            #     self.speechRecognitionThread.join()
            #     self.speechRecognitionThread.start()
            # self.someFoo(impl)


class SpeechToTextImpl(MTest.SpeechToTextListener):
    exemplar = None
    def setConstructor(self, main_class_exemplar):
        self.exemplar = main_class_exemplar

    def doAfterTextRecognition(self, recognizedText, isLast=False):
        print("Result: ", recognizedText)
        # recognizedObject = json.loads(recognizedText)
        # print("Result: ", recognizedObject["result"])
        # if isLast:
        #     self.exemplar.differentiatedAudioTrimList.pop(0)
        self.exemplar.isSpeechRecognized = True

class DifferentiatedAudioTrimImpl(AudioTrimListener):
    exemplar = None
    def setConstructor(self, main_class_exemplar):
        self.exemplar = main_class_exemplar

    def doAfterTrimL(self, list_of_trimmed_audio: BaseAudioStreamReceiver):
        self.exemplar.differentiatedAudioTrimList.append(list_of_trimmed_audio)


if __name__ == "__main__":
    print("Start program")
    basr = BaseAudioStreamReceiver()

    thread = Thread(target=basr.threadedAudioStream, args=())
    thread.start()

    tVoiceDiff = Thread(target=basr.threadVoiceDifferentiate, args=())
    tVoiceDiff.start()

    thread.join()
    tVoiceDiff.join()
