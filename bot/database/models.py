from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    discord_id = Column(Integer, unique=True, nullable=False)
    bio = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Отношения
    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")
    links = relationship("Link", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(discord_id={self.discord_id})>"


class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Отношения
    user = relationship("User", back_populates="projects")
    media = relationship("Media", back_populates="project", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Project(name={self.name}, category={self.category})>"


class Media(Base):
    __tablename__ = 'media'

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    url = Column(String(2048), nullable=False)
    type = Column(String(20), nullable=False)  # 'image', 'video', 'link'
    created_at = Column(DateTime, default=datetime.utcnow)

    # Отношения
    project = relationship("Project", back_populates="media")

    def __repr__(self):
        return f"<Media(type={self.type}, url={self.url})>"


class Link(Base):
    __tablename__ = 'links'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    url = Column(String(2048), nullable=False)
    title = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Отношения
    user = relationship("User", back_populates="links")

    def __repr__(self):
        return f"<Link(url={self.url}, title={self.title})>"


def register_models(engine=None):
    """Регистрирует все модели в базе данных"""
    if not engine:
        engine = create_engine("sqlite:///portfolio.db", echo=False)
        
    Base.metadata.create_all(engine) 