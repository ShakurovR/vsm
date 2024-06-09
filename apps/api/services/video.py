from core.service import generate_services
from fastapi import HTTPException, status
from models import Video
from schemas import VideoCreate, VideoRead, VideoReadList, VideoUpdate
from sqlalchemy.orm import Session

(
    _,
    get_one,
    get_all,
    find_one,
    find_all,
    update,
    delete,
    count,
) = generate_services(
    db_model=Video,
    create_schema=VideoCreate,
    read_schema=VideoRead,
    read_list_schema=VideoReadList,
    update_schema=VideoUpdate,
)


def get_by_task_id(db: Session, current_task: str) -> Video:
    try:
        result = db.query(Video).filter(Video.current_task == current_task).first()
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
        )
    return result


def get_by_checksum(db: Session, checksum: str) -> Video:
    try:
        result = db.query(Video).filter(Video.checksum == checksum).first()
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
        )
    return result
