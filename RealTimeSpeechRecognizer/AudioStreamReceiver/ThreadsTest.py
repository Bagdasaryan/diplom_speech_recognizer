from threading import Thread
import time
from RealTimeSpeechRecognizer.VoiceDifferentiation.Differentiation import VDifferentiation
from pydub import AudioSegment

class A:
    isT1Active = False

    def trim_audio(self, intervals, input_file_path, output_file_path):
        # load the audio file
        audio = AudioSegment.from_file(input_file_path)

        # iterate over the list of time intervals
        for i, (start_time, end_time) in enumerate(intervals):
            # extract the segment of the audio
            segment = audio[start_time * 1000:end_time * 1000]

            # construct the output file path
            output_file_path_i = f"{output_file_path}_{i}.wav"

            # export the segment to a file
            segment.export(output_file_path_i, format='wav')

if __name__ == "__main__":
    print("Start")
    a1 = A()
    a1.trim_audio([[0.5,2.0], [2.0, 3.3]], "1682960874.7695477.wav", "res")
