from app import celery_app
from celery.signals import worker_process_init
from celery import shared_task
import faster_whisper as fw
import os
import numpy as np
import io
import subprocess

model = None
compute_type = 'float16'
model_name = "large-v2"
device="cuda"

def load_audio(file: str, channel: int = None, sr: int = 16000):
    # left = 0 / right = 1
    try:
        # Launches a subprocess to decode audio while down-mixing and resampling as necessary.
        # Requires the ffmpeg CLI to be installed.
        cmd = [
            "ffmpeg",
            "-nostdin",
            "-threads",
            "0",
            "-i",
            file,
        ]
        if channel:
            cmd.append("-map_channel")
            cmd.append(f"0.0.{channel}")
        cmd += [
            "-f",
            "s16le",
            "-ac",
            "1",
            "-acodec",
            "pcm_s16le",
            "-ar",
            str(sr),
            "-",
        ]

        out = subprocess.run(cmd, capture_output=True, check=True).stdout
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}") from e

    return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0


def init_model(**kwargs):
    print("Initializing the model...")
    global model
    model = fw.WhisperModel(model_name, device, compute_type=compute_type,flash_attention=True)
    print("Initialization complete")


@shared_task(name='transcribe_file', bind=True)
def transcribe(self, fpath: str, language=None):
    if(model is None):
        init_model()
    audio = load_audio(fpath)
    # Deserialize to numpy array
    print("Starting transcribing...")
    tr_result, info = model.transcribe(
        audio,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=500),
        #word_timestamps=True,
        #language=language,
    )
    return (list(tr_result), info)