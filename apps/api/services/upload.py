import os
from pathlib import Path

import requests
from celery_apps import indexer_task, uploader_task
from core.logging import log
from core.schema import TaskResult
from core.settings import get_settings
from fastapi import HTTPException, UploadFile, status
from models import Video
from schemas import UploadTask, VideoRead
from simple_file_checksum import get_checksum
from sqlalchemy.orm import Session

from .video import get_by_checksum


def replace_file(tmppath: str) -> tuple[str, str]:
    settings = get_settings()
    try:
        # перемещаем видео
        checksum = get_checksum(tmppath)
        log.info(f"File checksum {checksum}")
        filedir = str(Path(settings.app_dir, settings.api_media_path, checksum))
        filepath = str(
            Path(settings.app_dir, settings.api_media_path, checksum, "source.mp4")
        )
        if not os.path.exists(filedir):
            os.mkdir(filedir)
        os.replace(tmppath, filepath)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error download file: {error}",
        )
    return (filepath, checksum)


def _save_file(file: UploadFile) -> tuple[str, str]:
    settings = get_settings()
    tmppath = str(Path(settings.app_dir, settings.api_media_path, file.filename))
    # скачиваем видео
    try:
        contents = file.file.read()
        with open(tmppath, "wb") as f:
            f.write(contents)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error download file: {error}",
        )
    finally:
        file.file.close()
    log.info("File uploaded")
    return replace_file(tmppath=tmppath)


def _upload_file(url: str) -> tuple[str, str]:
    settings = get_settings()
    tmppath = str(Path(settings.app_dir, settings.api_media_path, url.split("/")[-1]))
    # скачиваем видео
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(tmppath, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error download file: {error}",
        )
    log.info("File uploaded")
    return replace_file(tmppath=tmppath)


def _save_to_database(
    db: Session,
    filename: str,
    filepath: str,
    checksum: str,
    description: str,
    url: str | None = None,
) -> VideoRead:
    task_id, preview = indexer_task(
        "indexer.get_preview", filepath=filepath, wait_result=True
    )
    task_id, length = indexer_task(
        "indexer.get_length", filepath=filepath, wait_result=True
    )
    try:
        db_instance = get_by_checksum(db=db, checksum=checksum)
        if db_instance is None:
            db_instance = Video(
                name=filename,
                length=length,
                checksum=checksum,
                description=description,
                original_url=url,
            )
            log.info("Created new record in database")
            db.add(db_instance)
            db.commit()
            db.refresh(db_instance)
        else:
            log.info("Get exists record from database")
        log.info("Start to make index")
        task, _ = indexer_task(
            "indexer.file", filepath=filepath, video_id=db_instance.id
        )
        db_instance.current_task = task
        db.add(db_instance)
        db.commit()
    except Exception as error:
        print("DB error", str(error))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )
    return VideoRead.model_validate(db_instance)


def load_batch_from_csv(db: Session, csv_file: UploadFile) -> UploadTask:
    filepath, checksum = _save_file(file=csv_file)
    task, res = uploader_task("uploader.csv", csvfilepath=filepath)
    return TaskResult(task_id=task)


def load_single_from_url(db: Session, url: str, description: str) -> VideoRead:
    filepath, checksum = _upload_file(url=url)
    video = _save_to_database(
        db=db,
        filename=url.split("/")[-1],
        filepath=filepath,
        checksum=checksum,
        description=description,
        url=url,
    )
    return video


def load_single_from_file(
    db: Session, video_file: UploadFile, description: str
) -> VideoRead:
    filepath, checksum = _save_file(file=video_file)
    return _save_to_database(
        db=db,
        filename=video_file.filename[:-4],
        filepath=filepath,
        checksum=checksum,
        description=description,
    )
