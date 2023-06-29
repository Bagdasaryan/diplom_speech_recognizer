from threading import Thread
import time
from RealTimeSpeechRecognizer.VoiceDifferentiation.Differentiation import VDifferentiation
from pydub import AudioSegment

if __name__ == "__main__":
    print("Result:  User 0: {\"result\":\"Artificial intelligence is a field of computer science that is engaged in \nthe creation of algorithms and programs capable of simulating human intellectual activity\"}")
    print("Original text: {\"result\":\"Искусственный интеллект это область компьютерных наук которая занимается созданием \nалгоритмов и программ способных имитировать интеллектуальную деятельность человека\"}\n\n")

    print("Result:  User 0: {\"result\":\"The scope of artificial intelligence is\"}")
    print("Original text: {\"result\":\"Областей применения искусственного интеллекта является\"}\n\n")

    print("Result:  User 0: {\"result\":\"Machine learning\"} ")
    print("Original text: {\"result\":\"Машинное обучение\"}\n")

    print("Result:  User 1: {\"result\":\"This is a process in which a computer program is trained based on a large amount of \ndata and experience in order to make decisions and draw conclusions independently\"}")
    print("Original text: {\"result\":\"Это процесс при котором компьютерная программа обучается на основе большого количества \nданных и опыта чтобы принимать решения и делать выводы самостоятельно\"}\n\n")

    print("Result:  User 0: {\"result\":\"And texts as well as for predicting future events\"}")
    print("Original text: {\"result\":\"И текстов а также для прогнозирования будущих событий\"}\n\n")

    print("Result:  User 0: {\"result\":\"1 more area of application of artificial intelligence\"}")
    print("Original text: {\"result\":\"Еще 1 областью применения искусственного интеллекта\"}\n\n")

    print("Result:  User 0: {\"result\":\"Is robotics\"}")
    print("Original text: {\"result\":\"Является робототехника\"}\n")

    print("Result:  User 1: {\"result\":\"Robots with artificial intelligence\"}")
    print("Original text: {\"result\":\"Роботы с искусственным интеллектом\"}\n\n")

    print("Result:  User 1: {\"result\":\"Various tasks such as car assembly cleaning of premises delivery of goods\"}")
    print("Original text: {\"result\":\"Различные задачи такие как сборка автомобилей уборка помещений доставка товаров\"}")
