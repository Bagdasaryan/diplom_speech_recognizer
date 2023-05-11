import requests
import time


class SpeechToTextListener:
    def doAfterTextRecognition(self, recognizedText, isLast=False):
        pass


class MTest:
    def mFoo(self, fileName, listener: SpeechToTextListener()):
        for i in range(len(fileName)):
            self.translateSpeechToText(fileName[i], listener, isLast=len(fileName)-1 == i)

    def translateSpeechToText(self, fileName, listener: SpeechToTextListener(), isLast=False):
        # FOLDER_ID = "b1g395ej0iqqcob4b562" # Идентификатор каталога
        # OAUTH_KEY = "AQVNy9xEpeS-2VHWRkl1gBHaRpmUwAVK4E3Mtr_B" # oAuth key
        #
        # audioFile = "D:/Program Files/JetBrains/Projects/RealTimeSpeechRecognizer/AudioStreamReceiver/%s" % fileName[0]
        #
        # with open(audioFile, "rb") as f:
        #     data = f.read()
        #
        # params = "&".join([
        #     "topic=general",
        #     "folderId=%s" % FOLDER_ID,
        #     "lang=en-US",
        #     "format=oggopus"
        # ])
        #
        # url = "https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?%s" % params
        # headers = {'Authorization': "Api-Key %s" % OAUTH_KEY}
        #
        # x = requests.post(url, headers = headers, data=data)

        # res = "User %s: %s"%(fileName[1] , x.text)
        res = "User %s" % (fileName[1])
        listener.doAfterTextRecognition(res, isLast=False)
