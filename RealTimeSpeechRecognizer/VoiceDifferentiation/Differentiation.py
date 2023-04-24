# 1. visit hf.co/pyannote/speaker-diarization and hf.co/pyannote/segmentation and accept user conditions (only if requested)
# 2. visit hf.co/settings/tokens to create an access token (only if you had to go through 1.)
# 3. instantiate pretrained speaker diarization pipeline
import torch
from pyannote.audio import Pipeline
import einops

class VDifferentiation:
    def differentiate(self, fileName):
        pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization",
                                            use_auth_token="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")

        # 4. apply pretrained pipeline
        diarization = pipeline(fileName)

        # 5. print the result
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
