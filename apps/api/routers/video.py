from celery_apps import indexer_status
from core.database import get_db
from core.router import generate_router
from core.schema import TaskStatus
from fastapi import Depends, HTTPException, Path, status
from schemas import VideoCreate, VideoRead, VideoReadList, VideoUpdate
from services import count_videos, delete_video, get_video, get_videos, update_video
from sqlalchemy.orm import Session

router = generate_router(
    get_db=get_db,
    create_schema=VideoCreate,
    read_schema=VideoRead,
    read_list_schema=VideoReadList,
    update_schema=VideoUpdate,
    func_create=None,
    func_get_one=get_video,
    func_get_all=get_videos,
    func_update=update_video,
    func_delete=delete_video,
    func_count=count_videos,
    prefix="/video",
    tags=["Видео (CRUD)"],
)


@router.get("/{id}/status", description="Статус индексирования видео")
def router_video_status(
    db: Session = Depends(get_db), id: int = Path(description="ID видеоролика")
) -> TaskStatus:
    video = get_video(db=db, id=id)
    if video is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Video not found"
        )
    result = indexer_status(task_id=video.current_task)
    if result is not None:
        return TaskStatus(status=result.get("status", "Неопределено"))
    else:
        return TaskStatus(status="Неизвестно")
