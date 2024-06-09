import os
from pathlib import Path

import ffmpeg
from celery import shared_task
from celery_apps import indexer_celery
from core.database import get_db
from services import create_frame, get_video
from services.pipeline import (
    get_audio,
    make_frames,
    make_frames_desc,
    make_vtt,
    save_to_vdb,
    stt,
)


@shared_task(name="indexer.get_length", bind=True)
def get_length(
    self,
    filepath: str,
) -> None:
    try:
        info = ffmpeg.probe(
            filename=filepath,
        )
        return int(float(info.get("format", {"duration": "0"}).get("duration", "0")))
    except Exception as e:
        print(str(e))


@shared_task(name="indexer.get_preview", bind=True)
def get_preview(
    self,
    filepath: str,
) -> None:
    preview_path = str(Path(Path(filepath).parent, "preview.png"))
    if os.path.exists(preview_path):
        return preview_path
    try:
        (
            ffmpeg.input(filepath, ss="00:00:03.000")
            .output(preview_path, vframes=1)
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        return preview_path
    except Exception as e:
        print(str(e))


@shared_task(name="indexer.file", bind=True)
def start(self, filepath: str, video_id: int) -> None:
    indexer_celery

    print(f"Start indexer {filepath=}")

    # получить аудиодорожку
    print("Start get audio")
    self.update_state(
        task_id=self.request.id,
        state="PROGRESS",
        meta={"status": "Получение аудиодорожки"},
    )
    audiopath = get_audio(filepath=filepath)
    print(f"Audio created: {audiopath}")

    # извлекаем текст
    print("Start get text")
    self.update_state(
        task_id=self.request.id,
        state="PROGRESS",
        meta={"status": "Формируем текст из аудио"},
    )
    language, jsondata = stt(audiopath=audiopath)
    print(f"JSON created. Count of elements: {len(jsondata)}")

    # формируем уникальные кадры
    print("Start get frames")
    self.update_state(
        task_id=self.request.id,
        state="PROGRESS",
        meta={"status": "Формируем кадры"},
    )
    frames = make_frames(videopath=filepath)
    print(f"Frames created. Count of frames: {len(frames)}")

    # формируем описание кадров и сохраняем в vdb
    print("Start get frames desc")
    self.update_state(
        task_id=self.request.id,
        state="PROGRESS",
        meta={"status": "Формируем описание кадров"},
    )

    db = get_db().__next__()
    print(f"Get video from DB by ID={video_id}")

    video = get_video(db=db, id=video_id)
    if video is None:
        return None

    frame_descs = make_frames_desc(frames=frames)
    for time, desc in frame_descs.items():
        create_frame(db=db, video_id=video.id, description=desc, time=time)
    print(f"Descriptions of frames created. Count of descriptions: {len(frame_descs)}")

    # сделать субтитры
    print("Start get vtt.")
    self.update_state(
        task_id=self.request.id,
        state="PROGRESS",
        meta={"status": "Формируем субтитры"},
    )
    vttpath = make_vtt(
        jsondata=jsondata,
        output_dir=str(Path(audiopath).parent),
        language=language,
        frame_descs=frame_descs,
    )
    print(f"VTT created: {vttpath}")

    # сохраняем векторы
    print("Save in vdb")
    self.update_state(
        task_id=self.request.id,
        state="PROGRESS",
        meta={"status": "Сохраняем векторы"},
    )
    vttpath = save_to_vdb(
        videodata=frame_descs,
        audiodata=jsondata,
        textdata=video.description,
        video_id=video.id,
        language=language,
    )
    print("Save to VDB completed")
    if video.original_url is not None:
        os.remove(filepath)
    video.is_indexed = True
    db.add(video)
    db.commit()
    db.refresh(video)
    db.close()
