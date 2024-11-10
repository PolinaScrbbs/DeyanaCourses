from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import DeclarativeBase, relationship
from enum import Enum as BaseEnum


class Base(DeclarativeBase):
    pass


class BaseEnum(BaseEnum):
    @classmethod
    async def get_values(cls):
        return [breed.value for breed in cls]


# Роли
class Role(BaseEnum):
    USER = "Пользователь"
    MENTOR = "Наставник"
    EDITOR = "Редактор"
    ADREEDER = "Согласовант"
    DEVELOPER = "Разработчик"
    ADMIN = "Администратор"
    HR = "HR-специалист"


# Должности
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    courses = relationship("Module", secondary="course_posts", back_populates="posts")
    users = relationship("User", back_populates="post")


# Пользователи
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    hashed_password = Column(String(512), nullable=False)
    email = Column(String(30), default=None, unique=True, nullable=True)
    role = Column(Enum(Role), default=Role.USER, nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    full_name = Column(String(40), nullable=False)

    post = relationship("Post", back_populates="users")
    created_courses = relationship("Course", back_populates="creator")
    developed_courses = relationship(
        "Course", secondary="course_developers", back_populates="developers"
    )
    modules = relationship(
        "Module", back_populates="mentor", foreign_keys="[Module.mentor_id]"
    )
    tokens = relationship("Token", back_populates="user")

    course_results = relationship("CourseResult", back_populates="user")
    module_results = relationship("ModuleResult", back_populates="user")
    event_results = relationship("EventResult", back_populates="user")


# Токены для авторизации
class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True)
    token = Column(String(256), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="tokens")
