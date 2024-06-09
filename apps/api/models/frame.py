from core.database import Base
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Frame(Base):
    __tablename__ = "frame"

    id = Column(Integer, primary_key=True, index=True)

    video_id = Column(Integer, ForeignKey("video.id"))
    video = relationship(
        "Video", foreign_keys="[Frame.video_id]", back_populates="frames"
    )

    description = Column(String, nullable=True)
    time = Column(Float, nullable=True)
