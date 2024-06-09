from core.database import get_db
from fastapi import APIRouter, Depends, Path
from schemas import VideoRead
from services import index_video
from sqlalchemy.orm import Session

router = APIRouter(prefix="/index", tags=["Индексирование"])


@router.get("/{id}", description="Одиночная индексация по ID")
def route_index_video(
    id: int = Path(description="Идентификатор видеоролика"),
    db: Session = Depends(get_db),
) -> VideoRead:
    result = index_video(db=db, id=id)
    return result
