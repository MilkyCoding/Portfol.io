import os
import logging
import aiohttp
from datetime import datetime
from urllib.parse import urlparse
from typing import Optional

logger = logging.getLogger(__name__)

class MediaUtils:
    def __init__(self, media_dir: str = "media"):
        """Инициализация утилит для работы с медиафайлами
        
        Args:
            media_dir (str): Директория для хранения медиафайлов
        """
        self.media_dir = media_dir
        if not os.path.exists(self.media_dir):
            os.makedirs(self.media_dir)

    async def download_media(self, url: str, project_id: int) -> str:
        """Скачивает медиафайл и возвращает локальный путь
        
        Args:
            url (str): URL медиафайла
            project_id (int): ID проекта
            
        Returns:
            str: Локальный путь к скачанному файлу
            
        Raises:
            Exception: При ошибке скачивания файла
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        # Получаем расширение файла из URL
                        parsed_url = urlparse(url)
                        file_ext = os.path.splitext(parsed_url.path)[1]
                        if not file_ext:
                            content_type = response.headers.get('content-type', '')
                            if 'image' in content_type:
                                file_ext = '.png'
                            elif 'video' in content_type:
                                file_ext = '.mp4'
                            else:
                                file_ext = '.bin'

                        # Создаем уникальное имя файла
                        filename = f"{project_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}{file_ext}"
                        filepath = os.path.join(self.media_dir, filename)

                        # Сохраняем файл
                        with open(filepath, 'wb') as f:
                            f.write(await response.read())
                        
                        return filepath
        except Exception as e:
            logger.error(f"Ошибка при скачивании медиафайла: {str(e)}")
            raise

    @staticmethod
    def get_media_type(content_type: Optional[str]) -> Optional[str]:
        """Определяет тип медиафайла по content-type
        
        Args:
            content_type (Optional[str]): Content-type файла
            
        Returns:
            Optional[str]: Тип медиафайла ('image' или 'video') или None если тип не поддерживается
        """
        if not content_type:
            return None
            
        if 'image' in content_type:
            return 'image'
        elif 'video' in content_type:
            return 'video'
        return None 