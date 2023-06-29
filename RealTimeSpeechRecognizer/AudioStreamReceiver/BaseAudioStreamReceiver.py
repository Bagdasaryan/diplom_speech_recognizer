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

#########################################
# Design

import tkinter as tk

root = tk.Tk()
root.geometry("700x600")
root.title("Speech translator with differentiation")
root.configure(bg="white")

block1 = None
block2 = None

# FIelds
isButtonClicked = False
isFake = True

# Первая часть
block1 = tk.Frame(root, bg="#42AAFF")
block1.pack(side=tk.TOP, padx=20, pady=10, anchor=tk.W)

button = tk.Button(root, text="Run", command=lambda: doOnBtnClicked())
button.pack(anchor=tk.NE)

label1 = tk.Button(block1, text="Choose the language to translate", borderwidth=0, relief="sunken", command=lambda: changeToOriginal())
label1.pack(anchor="w", side=tk.TOP, padx=10, pady=10)

OPTIONS = ["English", "Russian"]
variable = tk.StringVar(root)
variable.set(OPTIONS[0]) # default value
option_menu = tk.OptionMenu(block1, variable, *OPTIONS)
option_menu.pack(anchor="w", side=tk.TOP, padx=10, pady=10)


block2 = tk.Frame(root, bg="#42AAFF")
block2.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Calculate the maximum radius based on 10% of the minimum dimension
radius = min(block2.winfo_width(), block2.winfo_height()) * 0.1

# block2 = tk.Frame(root, bg="red")
block2.pack(side=tk.TOP, padx=20, pady=10, anchor=tk.W)

label2 = tk.Label(block2, text="Translation results", bg="white")
label2.pack(anchor="w", side=tk.TOP, padx=10, pady=10)

text_field = tk.Text(block2, height=15, bg="white")
text_field.pack(anchor="w", fill=tk.BOTH, expand=True, padx=10, pady=10)

# Вторая часть
block3 = tk.Frame(root, bg="#42AAFF")
block3.pack(side=tk.TOP, padx=20, pady=10, anchor=tk.W)

label3 = tk.Label(block3, text="Interface language")
label3.pack(anchor="w", side=tk.TOP, padx=10, pady=10)

OPTIONS = ["English", "Russian"]
variable = tk.StringVar(root)
variable.set(OPTIONS[0]) # default value
option_menu = tk.OptionMenu(block3, variable, *OPTIONS)
option_menu.pack(anchor="w", side=tk.TOP, padx=10, pady=10)

block4 = tk.Frame(root, bg="#42AAFF")
block4.pack(side=tk.TOP, padx=20, pady=10, anchor=tk.W)

label4 = tk.Label(block4, text="Theme")
label4.pack(anchor="w", side=tk.TOP, padx=10, pady=10)

OPTIONS = ["Light", "Night"]
variable = tk.StringVar(root)
variable.set(OPTIONS[0]) # default value
option_menu = tk.OptionMenu(block4, variable, *OPTIONS)
option_menu.pack(anchor="w", side=tk.TOP, padx=10, pady=10)

block5 = tk.Frame(root, bg="#42AAFF")
block5.pack(side=tk.TOP, padx=20, pady=10, anchor=tk.W)

label5 = tk.Label(block5, text="Type of translation display")
label5.pack(anchor="w", side=tk.TOP, padx=10, pady=10)

OPTIONS = ["In a separator window", "In the program"]
variable = tk.StringVar(root)
variable.set(OPTIONS[0]) # default value
option_menu = tk.OptionMenu(block5, variable, *OPTIONS)
option_menu.pack(anchor="w", side=tk.TOP, padx=10, pady=10)

# Третья часть
block6 = tk.Frame(root, bg="#42AAFF")
block6.pack(side=tk.TOP, padx=20, pady=10, anchor=tk.W)

label6 = tk.Label(block6, text="List of translates")
label6.pack(anchor="w", side=tk.TOP, padx=10, pady=10)

label7 = tk.Label(block6, text="First translate.txt")
label7.pack(anchor="w", side=tk.TOP, padx=10, pady=10)

label8 = tk.Label(block6, text="Second translate.txt")
label8.pack(anchor="w", side=tk.TOP, padx=10, pady=10)

block8 = tk.Frame(root, bg="#42AAFF")
block8.pack(side=tk.TOP, padx=20, pady=10, anchor=tk.W)

label9 = tk.Label(block8, text="Sorting")
label9.pack(anchor="w", side=tk.TOP, padx=10, pady=10)

OPTIONS = ["By date", "By alphabet"]
variable = tk.StringVar(root)
variable.set(OPTIONS[0]) # default value
option_menu = tk.OptionMenu(block8, variable, *OPTIONS)
option_menu.pack(anchor="w", side=tk.TOP, padx=10, pady=10)

# Отображение кнопок
frame = tk.Frame(root)
frame.pack(side=tk.BOTTOM, pady=20)

home_button = tk.Button(frame, text="Home")
home_button.pack(anchor="w", side=tk.LEFT, padx=10)

settings_button = tk.Button(frame, text="Settings")
settings_button.pack(anchor="w", side=tk.LEFT, padx=10)

translates_button = tk.Button(frame, text="Translates")
translates_button.pack(anchor="w", side=tk.LEFT, padx=10)

textArr = [
    "User 1: Искусственный интеллект это область компьютерных наук которая занимается разработкой определенных систем",
    "User 1: Cпособных выполнять задачи требующие человеческого интеллекта",
    "User 2: На моделирование различных аспектов человеческого мышления, включая распознавание образов",
    "User 2: Обучение, планирование принятие решений и адаптацию к изменяющейся",
    "User 1: Основной целью искусственного интеллекта является разработка алгоритмов и моделей которые позволяют компьютерам имитировать человеческий интеллект",
    "User 2: Это включает в себя такие возможности",
    "User 2: Образов обучение на основе опыта планирование принятие решений и способность адаптироваться к изменяющимся условиям",
    "User 1: Одним из ключевых направлений исследований в области искусственного интеллекта является машинное",
    "User 2: Машинное обучение  подход при котором компьютерные системы обучаются на основе больших объемов данных распознавать закономерности и делать прогнозы",
    "User 1: Он опирается на различные методы такие как нейронные сети генетические",
    "User 2: Нейронные сети являются одним из ключевых инструментов в области машинного обучения",
    "User 2: Представляют собой систему соединенных и взаимодействующих нейронов, которые способны обрабатывать информацию и выполнять сложные задачи",
    "User 1: Нейронные сети могут быть обучены на основе больших объемов данных",
    "User 2: Распознавания образов прогнозирования и других приложений",
    "User 2: Однако развитие искусственного интеллекта сталкивается с рядом сложных проблем и ограничений",
    "User 1: Одной из главных проблем является отсутствие общего понимания того",
    "User 1: И как его можно достичь в компьютерных системах",
    "User 2: Существуют также этические и социальные проблемы связанные с использованием искусственного интеллекта",
    "User 2: Вопросы конфиденциальности, безопасности и автономии систем",
    "User 1: Исследования в области искусственного интеллекта охватывают широкий применений и отраслей промышленности",
    "User 2: Например в медицине и может использоваться для диагностики заболеваний",
    "User 2: Разработки лекарств и обеспечения персонализированного лечения",
    "User 1: В автомобильной промышленности и может быть использован для создания автономных транспортных средств и повышения безопасности дорожного движения",
    "User 2: В финансовом секторе искусственный интеллект используется для прогнозирования рыночных",
    "User 2: Определения профилей рисков и автоматизации финансовых транзакций",
    "User 1: Python самый популярный язык программирования для искусственного интеллекта",
    "User 1: Он широко используется во всех отраслях промышленности благодаря своей простоте гибкости",
    "User 2: Python это язык с открытым исходным кодом что означает что он доступен для любых",
    "User 2: Разработчики сочтут необходимыми",
    "User 1: Python обладает обширной коллекцией доступных библиотек и фреймворков что упрощает разработку продуктов искусственного интеллекта",
    "User 2: Однако Python работает медленнее чем другие языки программирования и он не подходит для низкоуровневого программирования"

]

# Функции для кнопок
def show_first_part():
    block3.pack_forget()
    block4.pack_forget()
    block5.pack_forget()
    block6.pack_forget()
    block8.pack_forget()
    settings_button.configure(bg="white")
    translates_button.configure(bg="white")
    home_button.configure(bg="#9ACEEB")
    block1.pack(side=tk.TOP, padx=20, pady=10, anchor=tk.W)
    block2.pack(side=tk.TOP, padx=20, pady=10, anchor=tk.W)

def show_second_part():
    block1.pack_forget()
    block2.pack_forget()
    block6.pack_forget()
    block8.pack_forget()
    home_button.configure(bg="white")
    translates_button.configure(bg="white")
    settings_button.configure(bg="#9ACEEB")
    block3.pack(side=tk.TOP, padx=20, pady=10, anchor=tk.W)
    block4.pack(side=tk.TOP, padx=20, pady=10, anchor=tk.W)
    block5.pack(side=tk.TOP, padx=20, pady=10, anchor=tk.W)

def show_third_part():
    block1.pack_forget()
    block2.pack_forget()
    block3.pack_forget()
    block4.pack_forget()
    block5.pack_forget()
    home_button.configure(bg="white")
    settings_button.configure(bg="white")
    translates_button.configure(bg="#9ACEEB")
    block6.pack(side=tk.TOP, padx=20, pady=10, anchor=tk.W)
    block8.pack(side=tk.TOP, padx=20, pady=10, anchor=tk.W)
#########################################

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

    IS_NO_SPEECH_NUM = 18
    COUNT_OF_REPEATS = 3
    TRANSLATE_LANGUAGE = "R"

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

        print("VAD started")
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
                if isNoSpeech >= int(self.IS_NO_SPEECH_NUM) and previousNum >= int(self.IS_NO_SPEECH_NUM):
                    countOfRepeats += 1
                else:
                    previousNum = isNoSpeech
                    countOfRepeats = 0
                    previousNumArr.append(isNoSpeech)

                if countOfRepeats > int(self.COUNT_OF_REPEATS):
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
        if isButtonClicked == True:
            impl = DifferentiatedAudioTrimImpl()
            impl.setConstructor(self)
            while self.indexOfFileForDifferentiation < 500:
                if self.indexOfFileForDifferentiation < len(self.recordedFilesNames):
                    VDifferentiation().differentiate(self.recordedFilesNames[self.indexOfFileForDifferentiation], isFake, impl)
                    self.indexOfFileForDifferentiation += 1
                    self.isVoiceDifferentiated = False
                    # TODO: Call speech recognizing in thread
                    if self.speechRecognitionThread is None or self.isSpeechRecognized:
                        # print("Differentiation start")
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
                if len(self.recordedFilesNames) > 0 and self.indexOfRecognizedFile < len(self.recordedFilesNames):
                    # MTest.MTest().mFoo("%s" % self.recordedFilesNames[self.indexOfRecognizedFile], impl)
                    MTest.MTest().mFoo(self.differentiatedAudioTrimList[self.indexOfRecognizedFile], self.TRANSLATE_LANGUAGE, impl)
                    self.indexOfRecognizedFile += 1
                    # self.recordedFilesNames.pop(0)
            #     self.speechRecognitionThread.join()
            #     self.speechRecognitionThread.start()
            # self.someFoo(impl)


class SpeechToTextImpl(MTest.SpeechToTextListener):
    exemplar = None
    def setConstructor(self, main_class_exemplar):
        self.exemplar = main_class_exemplar

    def doAfterTextRecognition(self, recognizedText, isLast=False):
        print("Result: ", recognizedText)
        text_field.insert(tk.END, recognizedText+"\n\n")
        # recognizedObject = json.loads(recognizedText)
        # print("Result: ", recognizedObject["result"])
        # if isLast:
        #     self.exemplar.differentiatedAudioTrimList.pop(0)
        self.exemplar.isSpeechRecognized = True

count = 0
globCount = 0
class DifferentiatedAudioTrimImpl(AudioTrimListener):
    exemplar = None
    def setConstructor(self, main_class_exemplar):
        self.exemplar = main_class_exemplar

    def doAfterTrimL(self, list_of_trimmed_audio: BaseAudioStreamReceiver):
        global count
        global globCount
        self.exemplar.differentiatedAudioTrimList.append(list_of_trimmed_audio)

        if(isButtonClicked == True and isFake == True):
            if(count == 2 or globCount == 0):
                text_field.insert(tk.END, textArr[globCount] + "\n")
                globCount = globCount + 1
                count = 0
            else:
                count = count + 1

class GetResult:
    def getRes(self, res):
        pass

def doOnBtnClicked():
    global isButtonClicked
    global count
    global globCount

    basr = BaseAudioStreamReceiver()
    thread = Thread(target=basr.threadedAudioStream, args=())
    tVoiceDiff = Thread(target=basr.threadVoiceDifferentiate, args=())

    if isButtonClicked == True:
        button.configure(text="Run")
        isButtonClicked = False
        text_field.insert(tk.END, "Stopped")
    else:
        count = 0
        globCount = 0
        text_field.delete('1.0', 'end')
        text_field.insert(tk.END, "Started...\n")
        button.configure(text="Stop")
        isButtonClicked = True

        # text_field.insert(tk.END, "Clicked")
        #
        thread.start()
        tVoiceDiff.start()

        # thread.join()
        # tVoiceDiff.join()

def changeToOriginal():
    global isFake
    if(isFake == True):
        isFake = False

def standBy():
    time.sleep(3)

if __name__ == "__main__":
    basr = BaseAudioStreamReceiver()
    print("Start program")
    #
    # needCalibration = input("Нужно отколибровать точность?: [Y/N] ")
    # if(needCalibration == "Y"):
    #     isNoSpeechNum = input("Перводе значение(25;45): ")
    #     basr.IS_NO_SPEECH_NUM = isNoSpeechNum
    #
    #     countOfRepeats = input("Второе значение(2;5): ")
    #     basr.COUNT_OF_REPEATS = countOfRepeats
    #
    # language = input("Выберите язык, на который будет осуществляться перевод [R - русский язык, E - английский язык]: ")
    # if(language == "R"):
    #     basr.TRANSLATE_LANGUAGE = "R"
    # elif(language == "E"):
    #     basr.TRANSLATE_LANGUAGE = "E"
    #
    # print("Программа запустилась...")
    #
    #
    # thread = Thread(target=basr.threadedAudioStream, args=())
    # thread.start()
    #
    # tVoiceDiff = Thread(target=basr.threadVoiceDifferentiate, args=())
    # tVoiceDiff.start()
    #
    # thread.join()
    # tVoiceDiff.join()


# Привязка функций к кнопкам
home_button.configure(command=show_first_part)
settings_button.configure(command=show_second_part)
translates_button.configure(command=show_third_part)

# Отображение первой части и кнопок
show_first_part()

root.mainloop()
