from core.database import get_db
from fastapi import APIRouter, Body, Depends, File, UploadFile
from schemas import VideoRead
from services import load_batch_from_csv, load_single_from_file, load_single_from_url
from sqlalchemy.orm import Session
from core.schema import TaskResult, TaskStatus
from celery_apps import uploader_status

router = APIRouter(prefix="/upload", tags=["Загрузка данных"])


@router.post("/csv", description="Пакетная загрузка из файла CSV (формат датасета)")
def router_csv(
    db: Session = Depends(get_db),
    upload_file: UploadFile = File(description="Файл CSV"),
) -> TaskResult:
    return load_batch_from_csv(db=db, csv_file=upload_file)


@router.get(
    "/csv/status", description="Статус пакетной загрузки по ID задания в процентах"
)
def router_csv_status(task_id: str) -> TaskStatus:
    result = uploader_status(task_id=task_id)
    return TaskStatus(status=result.get("status", "Неопределено"))


@router.post("/url", description="Одиночная загрузка по URL")
def router_url(
    db: Session = Depends(get_db),
    description: str = Body(description="Описание файла, с хештегами"),
    url: str = Body(description="Ссылка на видео"),
) -> VideoRead:
    return load_single_from_url(db=db, url=url, description=description)


@router.post("/file", description="Одиночная загрузка из файла")
def router_file(
    db: Session = Depends(get_db),
    description: str | None = Body(
        description="Описание файла, с хештегами", default=None
    ),
    upload_file: UploadFile = File(description="Файл видеоролика"),
) -> VideoRead:
    return load_single_from_file(db=db, video_file=upload_file, description=description)
