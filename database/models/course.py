from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

from .module import Base

# Связанная таблица для разработчиков курса
course_developers = Table(
    "course_developers",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("course_id", Integer, ForeignKey("courses.id"), primary_key=True),
)

# Связанная таблица для должностей, которым доступен курс
course_posts = Table(
    "course_posts",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id"), primary_key=True),
    Column("module_id", Integer, ForeignKey("modules.id"), primary_key=True),
)


# Курс
class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    title = Column(String(50), unique=True, nullable=False)
    description = Column(String(256), nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    creator = relationship("User", back_populates="created_courses")
    developers = relationship(
        "User", secondary="course_developers", back_populates="developed_courses"
    )
    modules = relationship("Module", back_populates="course")
    results = relationship("CourseResult", back_populates="course")
    posts = relationship("Post", secondary="course_posts", back_populates="courses")
