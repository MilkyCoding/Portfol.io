from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError
from typing import Optional, List
from datetime import datetime
import logging

from .models import User, Project, Media, Link, register_models

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, db_url: str = "sqlite:///portfolio.db"):
        self.engine = create_engine(db_url, echo=False)
        self.SessionLocal = sessionmaker(bind=self.engine)
        
        register_models()

    def get_session(self) -> Session:
        return self.SessionLocal()

    # User methods
    def get_user(self, discord_id: int) -> Optional[User]:
        try:
            with self.get_session() as session:
                return session.query(User).filter(User.discord_id == discord_id).first()
        except Exception as e:
            self._handle_error(e, "получении пользователя")

    def create_user(self, discord_id: int) -> User:
        try:
            with self.get_session() as session:
                user = User(discord_id=discord_id)
                session.add(user)
                session.commit()
                session.refresh(user)
                
                return user
        except Exception as e:
            self._handle_error(e, "создании пользователя")

    def update_user_bio(self, discord_id: int, bio: str) -> Optional[User]:
        try:
            with self.get_session() as session:
                user = session.query(User).filter(User.discord_id == discord_id).first()
                
                if user:
                    user.bio = bio
                    user.updated_at = datetime.utcnow()
                    session.commit()
                    session.refresh(user)
                    
                return user
        except Exception as e:
            self._handle_error(e, "обновлении профиля пользователя")

    # Project methods
    def create_project(self, discord_id: int, name: str, category: str, description: str) -> Optional[Project]:
        try:
            with self.get_session() as session:
                user = session.query(User).filter(User.discord_id == discord_id).first()
                
                if not user:
                    user = self.create_user(discord_id)

                project = Project(
                    user_id=user.id,
                    name=name,
                    category=category,
                    description=description
                )
                
                session.add(project)
                session.commit()
                session.refresh(project)
                
                return project
        except Exception as e:
            self._handle_error(e, "создании проекта")

    def get_user_projects(self, discord_id: int) -> List[Project]:
        try:
            with self.get_session() as session:
                user = session.query(User).filter(User.discord_id == discord_id).first()
                
                if not user:
                    return []
                
                return session.query(Project).filter(Project.user_id == user.id).all()
        except Exception as e:
            self._handle_error(e, "получении проектов пользователя")

    def get_project_by_name(self, discord_id: int, project_name: str) -> Optional[Project]:
        try:
            with self.get_session() as session:
                user = session.query(User).filter(User.discord_id == discord_id).first()
                
                if not user:
                    return None
                
                return session.query(Project).filter(
                    Project.user_id == user.id,
                    Project.name.ilike(project_name)
                ).first()
        except Exception as e:
            self._handle_error(e, "поиске проекта по имени")

    # Media methods
    def add_media(self, project_id: int, url: str, media_type: str) -> Optional[Media]:
        try:
            with self.get_session() as session:
                media = Media(
                    project_id=project_id,
                    url=url,
                    type=media_type
                )
                
                session.add(media)
                session.commit()
                session.refresh(media)
                
                return media
        except Exception as e:
            self._handle_error(e, "добавлении медиафайла")

    def get_project_media(self, project_id: int) -> List[Media]:
        try:
            with self.get_session() as session:
                return session.query(Media).filter(Media.project_id == project_id).all()
        except Exception as e:
            self._handle_error(e, "получении медиафайлов проекта")

    # Link methods
    def add_link(self, discord_id: int, url: str, title: Optional[str] = None) -> Optional[Link]:
        try:
            with self.get_session() as session:
                user = session.query(User).filter(User.discord_id == discord_id).first()
                
                if not user:
                    user = self.create_user(discord_id)

                link = Link(
                    user_id=user.id,
                    url=url,
                    title=title
                )
                session.add(link)
                session.commit()
                session.refresh(link)
                
                return link
        except Exception as e:
            self._handle_error(e, "добавлении ссылки")

    def get_user_links(self, discord_id: int) -> List[Link]:
        try:
            with self.get_session() as session:
                user = session.query(User).filter(User.discord_id == discord_id).first()
                
                if not user:
                    return []
                
                return session.query(Link).filter(Link.user_id == user.id).all()
        except Exception as e:
            self._handle_error(e, "получении ссылок пользователя")

    def set_links(self, discord_id: int, links: list[tuple[str, str]]) -> list[Link]:
        """Установить новые ссылки для пользователя (заменяет все существующие)"""
        try:
            with self.get_session() as session:
                # Получаем или создаем пользователя
                user = session.query(User).filter(User.discord_id == discord_id).first()
                
                if not user:
                    user = self.create_user(discord_id)
                
                # Удаляем все существующие ссылки
                session.query(Link).filter(Link.user_id == user.id).delete()
                
                # Добавляем новые ссылки
                new_links = []
                
                for url, title in links:
                    link = Link(user_id=user.id, url=url, title=title)
                    session.add(link)
                    new_links.append(link)
                
                session.commit()
                return new_links
        except Exception as e:
            self._handle_error(e, "установке ссылок пользователя")
            raise 
        
    def _handle_error(self, e: Exception, operation: str) -> None:
        """Обработка ошибок базы данных"""
        if isinstance(e, IntegrityError):
            logger.error(f"Ошибка целостности данных при {operation}: {str(e)}")
        else:
            logger.error(f"Ошибка базы данных при {operation}: {str(e)}")
        raise e