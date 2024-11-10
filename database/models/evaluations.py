from datetime import datetime
from datetime import timezone
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from .result import Base


# Оценивание
class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True)
    mentor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    result_id = Column(Integer, ForeignKey("event_results.id"), nullable=False)
    is_correct = Column(Boolean, default=False, nullable=False)
    comment = Column(String(128), default=None, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))

    result = relationship("EventResult", back_populates="evaluation")
