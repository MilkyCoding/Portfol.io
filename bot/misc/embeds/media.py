from nextcord import Embed, Color
import os

class MediaEmbeds:
    @staticmethod
    def add_media_missing_args() -> Embed:
        return Embed(
            title="❌ Ошибка",
            description=(
                "Пожалуйста, укажите название проекта.\n"
                "Пример: `/add-media Название проекта`\n\n"
                "После этого вы сможете загрузить медиафайлы для проекта."
            ),
            color=Color.red()
        )

    @staticmethod
    def no_attachments() -> Embed:
        return Embed(
            title="❌ Ошибка",
            description=(
                "Пожалуйста, прикрепите медиафайлы к сообщению.\n"
                "Поддерживаемые форматы:\n"
                "• Изображения (PNG, JPG, GIF)\n"
                "• Видео (MP4, WebM)"
            ),
            color=Color.red()
        )

    @staticmethod
    def media_add_result(project_name: str, added: list, errors: list = None) -> Embed:
        embed = Embed(
            title="📎 Результат добавления медиафайлов",
            description=f"Проект: **{project_name}**",
            color=Color.green() if added else Color.red()
        )

        if added:
            embed.add_field(
                name="✅ Успешно добавлены",
                value="\n".join(added),
                inline=False
            )

        if errors:
            embed.add_field(
                name="❌ Ошибки",
                value="\n".join(errors),
                inline=False
            )

        return embed

    @staticmethod
    def media_list(project_name: str, media: list) -> Embed:
        embed = Embed(
            title="📎 Медиафайлы проекта",
            description=f"Выберите номер файла для удаления из проекта **{project_name}**:",
            color=Color.blue()
        )

        for i, m in enumerate(media, 1):
            embed.add_field(
                name=f"{i}. {os.path.basename(m.url)}",
                value=f"Тип: {m.type}",
                inline=False
            )

        return embed

    @staticmethod
    def media_removed(project_name: str) -> Embed:
        return Embed(
            title="✅ Файл удален",
            description=f"Медиафайл успешно удален из проекта **{project_name}**",
            color=Color.green()
        )

    @staticmethod
    def no_media_in_project(project_name: str) -> Embed:
        return Embed(
            title="❌ Ошибка",
            description=f"У проекта **{project_name}** нет медиафайлов.",
            color=Color.red()
        )