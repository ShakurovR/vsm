from pydantic import BaseModel, Field


class UploadTask(BaseModel):
    task_id: str = Field("Номер задачи для пакетной загрузки")


class UploadStatus(BaseModel):
    percent: int = Field("Статус пакетной загрузки в процентах")
