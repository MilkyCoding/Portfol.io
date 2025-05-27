from nextcord import Embed, Color, Member
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from bot.database.models import Link

@dataclass
class CommandInfo:
    """Информация о команде для справки"""
    name: str
    description: str
    example: Optional[str] = None

class ProfileEmbeds:
    # Константы для цветов
    SUCCESS_COLOR = Color.green()
    INFO_COLOR = Color.blue()
    
    # Константы для команд
    COMMANDS: Dict[str, List[CommandInfo]] = {
        "👤 Профиль": [
            CommandInfo("set-profile", "установить описание профиля", "Креативный дизайнер с 5-летним опытом"),
            CommandInfo("set-links", "установить внешние ссылки", "GitHub: github.com/username, Behance: behance.net/username"),
            CommandInfo("profile", "просмотреть профиль", "@пользователь")
        ],
        "📁 Проекты": [
            CommandInfo("add-project", "создать проект", "Веб-сайт Веб-разработка Современный сайт для компании"),
            CommandInfo("preview", "просмотреть портфолио", "@пользователь")
        ],
        "📎 Медиафайлы": [
            CommandInfo("add-media", "добавить медиафайлы"),
            CommandInfo("remove-media", "удалить медиафайлы")
        ]
    }

    @staticmethod
    def _format_links(links: List[Link]) -> str:
        """Форматирует список ссылок для отображения"""
        return "\n".join(f"• [{link.title or 'Ссылка'}]({link.url})" for link in links)

    @staticmethod
    def _format_command_list(commands: List[CommandInfo]) -> str:
        """Форматирует список команд для отображения"""
        return "\n".join(f"• `/{cmd.name} {cmd.example or ''}` - {cmd.description}" for cmd in commands)

    @classmethod
    def profile_view(cls, member: Member, bio: str, links: List[Link], is_own_profile: bool) -> Embed:
        """Создает ембед для просмотра профиля"""
        embed = Embed(
            title=f"👤 Профиль {member.display_name}",
            description=bio or "Нет описания",
            color=cls.INFO_COLOR
        )

        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)

        if links:
            embed.add_field(
                name="🔗 Ссылки",
                value=cls._format_links(links),
                inline=False
            )

        preview_cmd = "preview" if is_own_profile else f"preview @{member.name}"
        embed.add_field(
            name="📁 Портфолио",
            value=f"Используйте `/{preview_cmd}` для просмотра портфолио",
            inline=False
        )

        return embed

    @classmethod
    def profile_updated(cls, bio: str) -> Embed:
        """Создает ембед об успешном обновлении профиля"""
        return Embed(
            title="✅ Профиль обновлен",
            description="Описание вашего профиля успешно обновлено",
            color=cls.SUCCESS_COLOR
        ).add_field(
            name="Новое описание",
            value=bio,
            inline=False
        )

    @classmethod
    def links_updated(cls, added_links: List[str], errors: Optional[List[str]] = None) -> Embed:
        """Создает ембед об успешном обновлении ссылок"""
        embed = Embed(
            title="✅ Ссылки обновлены",
            description="Результат обновления ссылок:",
            color=cls.SUCCESS_COLOR
        )

        if added_links:
            embed.add_field(
                name="Успешно добавлены",
                value="\n".join(added_links),
                inline=False
            )

        if errors:
            embed.add_field(
                name="Ошибки",
                value="\n".join(errors),
                inline=False
            )

        return embed

    @classmethod
    def help_command(cls) -> Embed:
        """Создает ембед со справкой по командам"""
        embed = Embed(
            title="📚 Справка по командам",
            description="Список доступных команд для управления портфолио:",
            color=cls.INFO_COLOR
        )

        for category, commands in cls.COMMANDS.items():
            embed.add_field(
                name=category,
                value=cls._format_command_list(commands),
                inline=False
            )

        if category == "📎 Медиафайлы":
            embed.add_field(
                name="Поддерживаемые форматы",
                value="• Изображения (PNG, JPG, GIF)\n• Видео (MP4, WebM)",
                inline=False
            )

        embed.set_footer(text="Используйте /help для просмотра этого сообщения")
        return embed 