import os
from pathlib import Path
from typing import Optional

from core.settings import get_settings
from fastapi import File, UploadFile
from pydantic import BaseModel, ConfigDict, Field, validator

from .frame import FrameRead

SETTINGS = get_settings()


class VideoBase(BaseModel):
    name: str = Field(description="Имя файла")
    description: Optional[str] = Field(description="Описание файла", default=None)
    is_indexed: Optional[bool] = False
    length: Optional[int] = Field(description="Длина файла в секундах", default=None)
    checksum: Optional[str] = Field(
        description="Контрольная сумма файла (чтобы не обрабатывать повторно)",
        default=None,
    )
    frames: Optional[list[FrameRead]] = Field(
        description="Ключевые кадры", default=None
    )
    current_task: Optional[str] = Field(
        description="Текущая задача обработки в Celery", default=None
    )
    original_url: Optional[str] = Field(
        description="Если загрузка по url, сохраняем его, чтобы не хранить у себя файл",
        default=None,
    )

    @validator("frames", pre=True, always=True)
    def get_frames(cls, v: list, values: dict) -> list[dict[str, str | None]]:
        filedir = str(
            Path(
                SETTINGS.app_dir, SETTINGS.api_media_path, values["checksum"], "frames"
            )
        )
        for item in v:
            if os.path.exists(str(Path(filedir, f"{int(item.time)}.png"))):
                item.url = f"{SETTINGS.api_media_url}{values['checksum']}/frames/{int(item.time)}.png"
        return v


class VideoCreate(BaseModel):
    file: UploadFile = File(description="Файл содержащий ведоконтент")
    description: str = Field(description="Описание файла")


class VideoRead(VideoBase):
    id: int
    urls: Optional[dict] = None

    @validator("urls", pre=True, always=True)
    def get_urls(cls, v: dict, values: dict) -> dict[str, str | None]:
        urls = {
            "preview": "preview.png",
            "video": "source.mp4",
            "audio": "source.wav",
            "subtitle": "subtitle.vtt",
        }
        filedir = str(
            Path(SETTINGS.app_dir, SETTINGS.api_media_path, values["checksum"])
        )
        for key, url in urls.items():
            if os.path.exists(str(Path(filedir, url))):
                urls[key] = f"{SETTINGS.api_media_url}{values['checksum']}/{url}"
            else:
                if key == "video" and values.get("original_url") is not None:
                    urls[key] = values.get("original_url")
                else:
                    urls[key] = None
        return urls

    model_config = ConfigDict(from_attributes=True)


class VideoReadWithFilepath(VideoRead):
    files: Optional[dict] = None

    @validator("files", pre=True, always=True)
    def get_files(cls, v: dict, values: dict) -> dict[str, str | None]:
        files = {
            "preview": "preview.png",
            "video": "source.mp4",
            "audio": "source.wav",
            "subtitle": "subtitle.vtt",
        }
        filedir = str(
            Path(SETTINGS.app_dir, SETTINGS.api_media_path, values["checksum"])
        )
        for key, fl in files.items():
            files[key] = (
                str(Path(filedir, fl))
                if os.path.exists(str(Path(filedir, fl)))
                else None
            )
        return files

    model_config = ConfigDict(from_attributes=True)


class VideoReadList(BaseModel):
    id: int
    name: str
    length: int
    is_indexed: Optional[bool] = False
    checksum: Optional[str]
    preview: Optional[str] = None

    @validator("preview", pre=True, always=True)
    def make_files(cls, v: str, values: dict):
        filedir = str(
            Path(SETTINGS.app_dir, SETTINGS.api_media_path, values["checksum"])
        )
        preview = os.path.exists(str(Path(filedir, "preview.png")))
        return (
            f"{SETTINGS.api_media_url}{values['checksum']}/preview.png"
            if preview
            else None
        )

    model_config = ConfigDict(from_attributes=True)


class VideoUpdate(BaseModel):
    name: str | None = None


class VideoSearchResultList(VideoReadList):
    video: str | None
    score: float


class VideoSearchResultReason(BaseModel):
    type_data: str
    content: str
    url: str | None = None
    score: float


class VideoSearchResult(BaseModel):
    name: str
    description: Optional[str] = None
    length: Optional[int] = None
    checksum: Optional[str] = None
    url: Optional[str] = None
    score: float
    reasons: list[VideoSearchResultReason]

    @validator("url", pre=True, always=True)
    def make_url(cls, v: str, values: dict):
        filedir = str(
            Path(SETTINGS.app_dir, SETTINGS.api_media_path, values["checksum"])
        )
        if os.path.exists(str(Path(filedir, "source.mp4"))):
            url = f"{SETTINGS.api_media_url}{values['checksum']}/source.mp4"
        else:
            if values.get("original_url") is not None:
                url = values.get("original_url")
            else:
                url = None
        return url
