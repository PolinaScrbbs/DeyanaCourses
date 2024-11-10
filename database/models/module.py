from sqlalchemy import (
    CHAR,
    Column,
    Integer,
    String,
    ForeignKey,
    Enum,
    Table,
    CheckConstraint,
    Boolean,
)
from sqlalchemy.orm import relationship
from enum import Enum as BaseEnum

from .user import Base

# Содержание собития
event_contents = Table(
    "event_contents",
    Base.metadata,
    Column("event_id", Integer, ForeignKey("events.id"), primary_key=True),
    Column("content_id", Integer, ForeignKey("contents.id"), primary_key=True),
)


# Тип события
class EventType(BaseEnum):
    THEORY = "Теория"
    PRACTICE = "Практика"
    ENTRANCE_CERTIFICATION = "Входная аттестация"
    FINAL_CERTIFICATION = "Итоговая аттестация"


# Табличка для хранения путей к файлам
class Content(Base):
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True)
    file_path = Column(String(256), unique=True, nullable=False)

    events = relationship(
        "Event", secondary="event_contents", back_populates="contents"
    )


# Событие
class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)

    title = Column(String(50), unique=True, nullable=False)
    description = Column(String(256), nullable=False)
    type = Column(Enum(EventType), default=EventType.THEORY, nullable=False)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)

    module = relationship("Module", back_populates="events")
    contents = relationship(
        "Content", secondary="event_contents", back_populates="events"
    )
    results = relationship("EventResult", back_populates="event")


# Модуль
class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True)
    code = Column(CHAR(8), nullable=False)
    title = Column(String(50), unique=True, nullable=False)
    description = Column(String(256), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    mentor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    number = Column(Integer, nullable=False)
    duration_days = Column(Integer, nullable=False)
    is_draft = Column(Boolean, default=True, nullable=False)

    __table_args__ = (
        CheckConstraint("duration_days > 0", name="positive_duration_days"),
        CheckConstraint("number > 0", name="positive_module_number"),
    )

    course = relationship("Course", back_populates="modules")
    events = relationship("Event", back_populates="module")
    results = relationship("ModuleResult", back_populates="module")
    mentor = relationship("User", foreign_keys=[mentor_id])
