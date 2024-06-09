import base64
import json
import os
import re
import subprocess

import googletrans
import numpy as np
import requests

prompt = """[INST] You are an expert image analyzing system. You will give precise and relevant information about the picture.
Give me description of the image, try to make it as short as possible without losing quality
[/INST]
The image shows"""

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


def encode_image(framepath: str) -> str:
    with open(framepath, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def request_description(framepath: str) -> str:  # -> Any:
    base64_image = encode_image(framepath)
    url = os.getenv("LLAMA_URL", "http://llama:8080/completion")
    headers = {"Content-Type": "application/json"}
    data = {
        "prompt": prompt,
        "n_predict": 108,
        "image_data": [{"data": base64_image, "id": 10}],
        "temperature": 0,
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    data_dict = json.loads(response.text)
    content = data_dict["content"]
    return content


def clean_words_existence(text: str) -> str:
    phrases = [
        "ASSISTANT: Certainly!",
        "ASSISTANT: Sure, ",
        "USER: Can you tell me more about the image?",
        "Hello! How can I assist you today?",
        "Certainly!",
        "ASSISTANT: ",
        "USER: ",
        ", feel free to ask!",
    ]
    for phrase in phrases:
        text = text.replace(phrase, "")
    return text


def check_words_existence(text):
    blacklist = [
        "sorry",
        "assist",
        "with",
        "specific",
        "questions",
        "about",
        "scene",
        "objects",
        "help",
    ]
    words_in_text = re.findall(r"\w+", text.lower())
    word_existence = [word in words_in_text for word in blacklist]
    blacklist_count = sum(word_existence)
    if (blacklist_count / len(blacklist)) >= 0.7:
        return True
    else:
        return False


def translation(text) -> str:
    translator = googletrans.Translator()
    response = translator.translate(text, src="ru", dest="en")
    return response.text
