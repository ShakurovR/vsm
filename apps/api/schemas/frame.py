from typing import Optional

from core.settings import get_settings
from pydantic import BaseModel, ConfigDict, Field

SETTINGS = get_settings()


class FrameBase(BaseModel):
    description: str = Field(description="Описание кадра")
    time: Optional[float] = Field(description="Время кадра на видео в секундах (float)")


class FrameRead(FrameBase):
    id: int
    url: str | None = None
    model_config = ConfigDict(from_attributes=True)
