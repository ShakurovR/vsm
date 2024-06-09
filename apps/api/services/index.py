import os

from celery_apps import indexer_task
from core.exception import NotFound
from schemas import VideoRead, VideoReadWithFilepath
from sqlalchemy.orm import Session

from .upload import _upload_file
from .video import get_one


def index_video(db: Session, id: int) -> VideoRead:
    video = get_one(db=db, id=id)
    if video is None:
        raise NotFound()
    if video.original_url is not None:
        _upload_file(url=video.original_url)

    video_path = VideoReadWithFilepath.model_validate(video)

    task, _ = indexer_task(
        "indexer.file",
        filepath=video_path.files.get("video"),
        video_id=video.id,
        wait_result=True,
    )

    video.current_task = task
    db.add(video)
    db.commit()
    db.refresh(video)
    os.remove(video_path.files.get("video"))
    return VideoRead.model_validate(video)
