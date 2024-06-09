from typing import Optional

from fastapi import HTTPException, status
from models import Frame
from schemas import FrameRead
from sqlalchemy.orm import Session


def create(db: Session, video_id: int, description: str, time: float) -> FrameRead:
    try:
        db_instance = get_frame_by_time_and_video(db=db, video_id=video_id, time=time)
        if db_instance is None:
            db_instance = Frame(video_id=video_id, description=description, time=time)
            db.add(db_instance)
            db.commit()
            db.refresh(db_instance)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )
    return db_instance


def get_frame_by_time_and_video(
    db: Session, video_id: int, time: float
) -> Optional[FrameRead]:
    try:
        result = (
            db.query(Frame)
            .filter(Frame.video_id == video_id, Frame.time == time)
            .first()
        )
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
        )
    return result
