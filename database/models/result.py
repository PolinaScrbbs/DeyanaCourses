from datetime import datetime
from datetime import timezone
from sqlalchemy import (
    Boolean,
    Column,
    Enum,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Time,
    CheckConstraint,
)
from sqlalchemy.orm import relationship
from enum import Enum as BaseEnum

from .course import Base


# Результаты курса
class CourseResult(Base):
    __tablename__ = "course_results"

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    started_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    end_at = Column(DateTime, default=None, nullable=True)
    execution_time = Column(Time, default=None, nullable=True)
    is_completed = Column(Boolean, default=False, nullable=False)

    completed_event_count = Column(Integer, default=0, nullable=False)
    completed_modules_count = Column(Integer, default=0, nullable=False)

    __table_args__ = (
        CheckConstraint(
            "completed_event_count >= 0", name="check_completed_events_count_positive"
        ),
        CheckConstraint(
            "completed_modules_count >= 0",
            name="check_completed_modules_count_positive",
        ),
    )

    course = relationship("Course", back_populates="results")
    user = relationship("User", back_populates="course_results")


# Результаты модуля
class ModuleResult(Base):
    __tablename__ = "module_results"

    id = Column(Integer, primary_key=True)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    started_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    end_at = Column(DateTime, default=None, nullable=True)
    is_completed = Column(Boolean, default=False, nullable=False)

    module = relationship("Module", back_populates="results")
    user = relationship("User", back_populates="module_results")


# Статусы для результата события
class EventResultStatus(BaseEnum):
    PROGRESS = "Выполняется"
    COMPLETED = "Выполнен"
    RATED = "Оценен"


# Результат события
class EventResult(Base):
    __tablename__ = "event_results"

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(
        Enum(EventResultStatus), default=EventResultStatus.COMPLETED, nullable=False
    )
    started_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    end_at = Column(DateTime, default=None, nullable=True)

    comment = Column(String(128), default=None, nullable=True)
    content = Column(String(512), nullable=False)

    event = relationship("Event", back_populates="results")
    user = relationship("User", back_populates="event_results")
    evaluation = relationship("Evaluation", back_populates="result")
