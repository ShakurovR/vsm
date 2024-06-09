from core.database import Base
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship


class Video(Base):
    __tablename__ = "video"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)
    description = Column(String, nullable=True)
    length = Column(Integer, nullable=True)
    is_indexed = Column(Boolean, default=False)
    checksum = Column(String, nullable=True)
    current_task = Column(String, nullable=True)
    frames = relationship("Frame", back_populates="video")
    original_url = Column(String, nullable=True)
