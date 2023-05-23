import requests

from typing import List


class SpeechToTextListener:
    def doAfterTextRecognition(self, recognizedText, isLast=False):
        pass


class MTest:
    FOLDER_ID = "b1g395ej0iqqcob4b562"  # Идентификатор каталога
    OAUTH_KEY = "AQVNy9xEpeS-2VHWRkl1gBHaRpmUwAVK4E3Mtr_B"  # oAuth key

    def mFoo(self, fileName, listener: SpeechToTextListener()):
        # translatedText = self.translate(
        #     texts=["Hello. How are you?", "Thanks. What are you doing?"],
        #     source="en",
        #     target="ru"
        # )
        # for i in range(len(translatedText)):
        #     print("Translate res: ", translatedText[i])

        for i in range(len(fileName)):
            self.translateSpeechToText(fileName[i], listener, isLast=len(fileName)-1 == i)
            # self.testTranslateSpeechToText(listener)

    def translateSpeechToText(self, fileName, listener: SpeechToTextListener(), isLast=False):
        audioFile = "D:/Program Files/JetBrains/Projects/RealTimeSpeechRecognizer/AudioStreamReceiver/%s" % fileName[0].replace("wav", "ogg")

        with open(audioFile, "rb") as f:
            data = f.read()

        params = "&".join([
            "topic=general",
            "folderId=%s" % self.FOLDER_ID,
            "lang=ru-RU", # en-US
            "format=oggopus"
        ])

        url = "https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?%s" % params
        headers = {'Authorization': "Api-Key %s" % self.OAUTH_KEY}

        x = requests.post(url, headers = headers, data=data)

        translatedText = self.translate(
            texts=[x.text],
            source="ru",
            target="en"
        )

        res = "User %s: %s" % (fileName[1], translatedText[0])

        # res = "User %s" % (fileName[0].replace("wav", "ogg"))
        listener.doAfterTextRecognition(res, isLast=False)

    def translate(self, texts: List[str], source: str, target: str) -> List[str]:
        api_key = "AQVN0gEwlgm1cN-za2i2qAqYbUIzyLKSARbqhidv"
        # Сформируем заголовок запроса с ключем авторизации
        headers = {
            "Authorization": f"Api-Key {api_key}",
        }

        # Отправим запрос
        res = requests.post(
            "https://translate.api.cloud.yandex.net/translate/v2/translate",
            json={
                "sourceLanguageCode": source,
                "targetLanguageCode": target,
                "format": "PLAIN_TEXT",
                "texts": texts,
            },
            headers=headers)

        print("TR: ", res)
        return [t["text"] for t in res.json()["translations"]]

    def testTranslateSpeechToText(self, listener: SpeechToTextListener()):
        listener.doAfterTextRecognition("TestRes", isLast=False)
