# 1. visit hf.co/pyannote/speaker-diarization and hf.co/pyannote/segmentation and accept user conditions (only if requested)
# 2. visit hf.co/settings/tokens to create an access token (only if you had to go through 1.)
# 3. instantiate pretrained speaker diarization pipeline
import torch
from pyannote.audio import Pipeline
from pydub import AudioSegment
import einops

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
            print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
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

        listener.doAfterTrimL(list_of_trimmed_audio)
