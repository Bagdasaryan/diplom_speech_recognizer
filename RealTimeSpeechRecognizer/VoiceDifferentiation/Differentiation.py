# 1. visit hf.co/pyannote/speaker-diarization and hf.co/pyannote/segmentation and accept user conditions (only if requested)
# 2. visit hf.co/settings/tokens to create an access token (only if you had to go through 1.)
# 3. instantiate pretrained speaker diarization pipeline
import os

import pyogg
import torch
from pyannote.audio import Pipeline
from pydub import AudioSegment
import einops
import wave

class AudioTrimListener:
    def doAfterTrimL(self, list_of_trimmed_audio):
        pass

class VDifferentiation:
    def differentiate(self, fileName, listener: AudioTrimListener()):
        pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization",
                                            use_auth_token="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")

        # 4. apply pretrained pipeline
        diarization = pipeline(fileName+".wav")

        # 5. print the result
        intervals = []
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            # print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
            interv = [turn.start, turn.end]
            intervals.append(interv)
        self.trim_audio(intervals, fileName, fileName, listener)

    def trim_audio(self, intervals, input_file_path, output_file_path, listener: AudioTrimListener()):
        list_of_trimmed_audio = [] # [audio_file_name, speaker_id]

        # load the audio file
        audio = AudioSegment.from_file(input_file_path+".wav")

        # iterate over the list of time intervals
        for i, (start_time, end_time) in enumerate(intervals):
            # extract the segment of the audio
            segment = audio[start_time * 1000:end_time * 1000]

            # construct the output file path
            output_file_path_i = f"res_{output_file_path}_{i}.wav"

            # export the segment to a file
            segment.export(output_file_path_i, format='wav')

            # 0 - first speaker; 1 - second speaker
            list_of_trimmed_audio.append([f"res_{output_file_path}_{i}.wav", 0 if i % 2 == 0 else 1])

            file_name = "res_%s_%s"%(output_file_path, i)

            try:
                self.save_to_opus(file_name)
            except:
                print("An exception occurred")

        listener.doAfterTrimL(list_of_trimmed_audio)

    def save_to_opus(self, filename):
        # Открытие аудиофайла
        with wave.open("%s.wav" % filename, "rb") as audio_file:
            # Получение параметров аудиофайла
            channels = audio_file.getnchannels()
            sample_width = audio_file.getsampwidth()
            frame_rate = audio_file.getframerate()
            frames = audio_file.readframes(-1)

        # Преобразование байтовых данных в массив байтов
        contents = bytearray(frames)

        # with open("%s.wav"%filename, 'rb') as fd:
        #     contents = fd.read()

        # Create a OpusBufferedEncoder
        opus_buffered_encoder = pyogg.OpusBufferedEncoder()
        opus_buffered_encoder.set_application("audio")
        opus_buffered_encoder.set_sampling_frequency(48000)
        opus_buffered_encoder.set_channels(1)
        opus_buffered_encoder.set_frame_size(20)  # milliseconds

        ogg_opus_writer = pyogg.OggOpusWriter(
            filename+".ogg",
            opus_buffered_encoder
        )

        # Encode the PCM data
        ogg_opus_writer.write(
            memoryview(bytearray(contents))
            # memoryview(bytearray(b''.join(contents)))
        )

        # opus_buffered_encoder = None

        # We've finished writing the file
        ogg_opus_writer.close()
