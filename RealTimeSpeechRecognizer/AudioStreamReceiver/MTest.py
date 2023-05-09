import requests
import time


class SpeechToTextListener:
    def doAfterTextRecognition(self, recognizedText):
        pass


class MTest:
    def mFoo(self, fileName, listener: SpeechToTextListener()):
        # FOLDER_ID = "b1g395ej0iqqcob4b562" # Идентификатор каталога
        # OAUTH_KEY = "AQVNy9xEpeS-2VHWRkl1gBHaRpmUwAVK4E3Mtr_B" # oAuth key
        #
        # audioFile = "D:/Program Files/JetBrains/Projects/RealTimeSpeechRecognizer/AudioStreamReceiver/%s" % fileName
        #
        # with open(audioFile, "rb") as f:
        #     data = f.read()
        #
        # params = "&".join([
        #     "topic=general",
        #     "folderId=%s" % FOLDER_ID,
        #     "lang=ru-RU",
        #     "format=oggopus"
        # ])
        #
        # url = "https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?%s" % params
        # headers = {'Authorization': "Api-Key %s" % OAUTH_KEY}
        #
        # x = requests.post(url, headers = headers, data=data)

        listener.doAfterTextRecognition("recognized file: %s"%fileName) # x.text)
        time.sleep(10)
