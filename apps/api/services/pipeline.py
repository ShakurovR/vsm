import os
import sys
from pathlib import Path

# import cv2
#import faster_whisper as fw
import ffmpeg
from chromadb import HttpClient
from celery_apps import indexer_celery
from celery.result import allow_join_result
# from imagededup.methods import PHash
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from .pipelineutils import (
    check_words_existence,
    clean_words_existence,
    load_audio,
    request_description,
    translation,
)

device = "cuda"
# device = "cuda" if torch.cuda.is_available() else "cpu"
# if device == "cuda":
#     model_name = "large-v2"
#     compute_type = "float16"
# else:
model_name = "large-v2"
compute_type = "float16"
#FW_MODEL = fw.WhisperModel(model_name, device, compute_type=compute_type)

CHROMA_EMB = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
    model_kwargs={"trust_remote_code": True},
)

# def init_worker_process(**kwargs):
#     print("Initializing the model...")
#     global model
#     model = fw.WhisperModel(model_name, device, compute_type=compute_type)
#     print("Initialization complete")


def get_frame(
    filepath: str,
    second: int,
) -> None:

    preview_path = str(Path(Path(filepath).parent, "frames", f"{second}.png"))
    if os.path.exists(preview_path):
        return preview_path
    h = int(second // 3600)
    m = int((second - 3600 * h) // 60)
    s = int(second - 3600 * h - m * 60)
    ms = int(second * 1000) % 1000
    try:
        (
            ffmpeg.input(filepath, ss=f"{h:02}:{m:02}:{s:02}.{ms:03}")
            .output(preview_path, vframes=1)
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        return preview_path
    except Exception as e:
        print(str(e))


def get_length(filepath: str) -> int:
    try:
        info = ffmpeg.probe(
            filename=filepath,
        )
        return int(float(info.get("format", {"duration": "0"}).get("duration", "0")))
    except ffmpeg.Error as e:
        print(e.stderr.decode(), file=sys.stderr)
        sys.exit(1)


def get_audio(filepath: str) -> str:
    # ffmpeg -i my_video.mp4 -c copy -map 0:a output_audio.mp4
    audio_path = str(Path(Path(filepath).parent, "source.wav"))
    if os.path.exists(audio_path):
        return audio_path
    try:
        (
            ffmpeg.input(filepath)
            .output(audio_path, format="wav", acodec="pcm_s16le", ac=1, ar="16000")
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        return audio_path
    except ffmpeg.Error as e:
        print(e.stderr.decode(), file=sys.stderr)
        sys.exit(1)


def stt(audiopath: str) -> tuple[str, list[dict[str, any]]]:
    global FW_MODEL
    # if "model" not in dir() or model is None:
    #     print("Models hasn't been initialized, loading...")
    #     init_worker_process()
    #audio = load_audio(audiopath)

    print("Sending file to transcribe...")
    task_transcr = indexer_celery.send_task(
            "transcribe_file",
            kwargs={
                'fpath':audiopath,
            },
            queue="transcriber"
            )
    print("Waiting for transcribe task...")
    with allow_join_result():
            (result, info) = task_transcr.get()
    print(f"{result[0]}")
    return (
        info[0],
        [
            {"start": segment[2], "end": segment[3], "text": segment[4].strip()}
            for segment in result
        ],
    )


def make_vtt(
    jsondata: list[dict[str, any]],
    language: str,
    output_dir: str,
    frame_descs: dict[float, str],
) -> str:
    def get_timing(second: float) -> str:
        mm, ss = divmod(int(second), 60)
        hh, mm = divmod(mm, 60)
        ms = int((second - int(second)) * 1000)
        return f"{hh:02}:{mm:02}:{ss:02}.{ms:03}"

    def find_notes(frame_descs: dict[float, str], starttime: float, endtime: float):
        items = [frame_descs[x] for x in frame_descs if x >= starttime and x < endtime]
        if len(items) == 0:
            return None
        else:
            return "\n".join(items)

    vttpath = str(Path(output_dir, "subtitle.vtt"))
    if os.path.exists(vttpath):
        return vttpath

    with open(vttpath, "w") as vtt:
        vtt.write("WEBVTT\n")
        vtt.write("Kind: captions\n")
        vtt.write(f"Language: {language}\n\n")
        for numline, line in enumerate(jsondata):
            print(f"Write {numline+1} line: {line['text']}")
            vtt.write(f"{numline+1}\n")
            vtt.write(f"{get_timing(line['start'])} --> {get_timing(line['end'])}\n")
            text = str(line["text"]).strip()
            vtt.write(f"{text}\n\n")
            if (
                notes := find_notes(frame_descs, line["start"], line["end"])
            ) is not None:
                vtt.write(f"NOTE {notes}\n\n")

    return vttpath


def make_frames(videopath: str) -> list[str]:
    unique_frames = {}
    output_dir = str(Path(Path(videopath).parent, "frames"))
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    length = get_length(filepath=videopath)
    diff = length // 3 if length < 30 else length // 5
    for time in range(0, length, diff):
        unique_frames[time] = get_frame(filepath=videopath, second=time)
    # требует доработки если успеем
    # phasher = PHash()
    # encodings = {}
    # unique_frames = {}
    # output_dir = str(Path(Path(videopath).parent, "frames"))

    # if not os.path.exists(output_dir):
    #     os.mkdir(output_dir)
    # cap = cv2.VideoCapture(videopath)
    # if not cap.isOpened():
    #     raise Exception("Error: Could not open video.")
    # fps = cap.get(cv2.CAP_PROP_FPS)
    # frame_count = 0
    # while True:
    #     ret, frame = cap.read()
    #     if not ret:
    #         break
    #     frame_seconds = frame_count / fps
    #     frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #     current_hash = phasher.encode_image(image_file=False, image_array=frame_rgb)
    #     is_duplicate = False
    #     for existing_hash in encodings.values():
    #         if phasher.hamming_distance(current_hash, existing_hash) <= 18:
    #             is_duplicate = True
    #             break
    #     if not is_duplicate:
    #         # Save unique frame
    #         encodings[frame_seconds] = current_hash
    #         frame_filename = f"{frame_seconds:.2f}.jpg"
    #         cv2.imwrite(str(Path(output_dir, frame_filename)), frame)
    #         unique_frames[frame_seconds] = str(Path(output_dir, frame_filename))
    #     frame_count += 1
    # cap.release()

    return [unique_frames[frame] for frame in unique_frames]


def make_frames_desc(frames: list) -> dict[float, str]:
    result = dict()
    for frame in frames:
        descr = request_description(frame)
        result[float(Path(frame).stem)] = descr
        #descr = clean_words_existence(descr)
        #if not check_words_existence(descr):
        #    result[float(Path(frame).stem)] = descr
    return result


def save_to_vdb(
    # vttpath: str,
    videodata: dict,
    audiodata: dict,
    textdata: str,
    video_id: int,
    language: str,
) -> None:
    global CHROMA_EMB
    data = []
    if len(videodata) > 0:
        for time in videodata:
            data.append(
                Document(
                    page_content=videodata[time],
                    metadata={
                        "video_id": video_id,
                        "type_data": "video",
                        "time": str(time),
                    },
                )
            )
    if len(audiodata) > 0:
        _audiodata = []
        if language != "en":
            for segment in audiodata:
                text = translation(segment["text"])
                _audiodata.append(
                    {
                        "start": str(segment["start"]),
                        "end": str(segment["end"]),
                        "text": str(text),
                    }
                )
        else:
            _audiodata = audiodata
        for segment in _audiodata:
            data.append(
                Document(
                    page_content=segment["text"],
                    metadata={
                        "video_id": video_id,
                        "type_data": "audio",
                        "time": str(segment["start"]),
                    },
                )
            )
    if textdata is not None:
        tags = []
        text = []
        for word in textdata.replace(" , ", " ").split(" "):
            if len(word) > 1:
                if word[0] == "#":
                    tags.append(word)
                else:
                    text.append(word)
        if text is not None and len(text) > 0:
            data.append(
                Document(
                    page_content=translation(" ".join(text)),
                    metadata={"video_id": video_id, "type_data": "text"},
                )
            )
        if tags is not None and len(tags) > 0:
            data.append(
                Document(
                    page_content=translation(" ".join(tags)),
                    metadata={"video_id": video_id, "type_data": "hashtag"},
                )
            )

    text_splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=20)
    chromaclient = HttpClient(host=os.getenv("CHROMA_HOST", "chroma"))

    Chroma.from_documents(
        text_splitter.split_documents(data),
        CHROMA_EMB,
        persist_directory="video",
        collection_metadata={"hnsw:space": "cosine"},
        client=chromaclient,
    ).persist()
