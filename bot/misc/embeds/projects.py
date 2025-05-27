from nextcord import Embed, Color
from datetime import datetime

class ProjectEmbeds:
    @staticmethod
    def add_project_missing_args() -> Embed:
        return Embed(
            title="❌ Ошибка",
            description=(
                "Пожалуйста, укажите все необходимые параметры.\n"
                "Пример: `/add-project Название Категория Описание проекта`\n\n"
                "• Название - короткое название проекта\n"
                "• Категория - например: Веб-разработка, Дизайн, Фото\n"
                "• Описание - подробное описание проекта"
            ),
            color=Color.red()
        )

    @staticmethod
    def project_limit_reached() -> Embed:
        return Embed(
            title="❌ Ошибка",
            description=(
                "У вас уже есть максимальное количество проектов (3).\n"
                "Удалите один из существующих проектов, чтобы добавить новый."
            ),
            color=Color.red()
        )

    @staticmethod
    def project_exists(name: str) -> Embed:
        return Embed(
            title="❌ Ошибка",
            description=f"Проект с названием **{name}** уже существует.",
            color=Color.red()
        )

    @staticmethod
    def project_added_success(name: str, category: str, description: str, remaining: int) -> Embed:
        embed = Embed(
            title="✅ Проект добавлен",
            description=f"**{name}** успешно добавлен в ваше портфолио",
            color=Color.green(),
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="Категория", value=category, inline=True)
        embed.add_field(name="Описание", value=description, inline=False)
        embed.add_field(
            name="Осталось проектов",
            value=f"Вы можете добавить еще {remaining} проект(а)",
            inline=False
        )
        embed.set_footer(text="Используйте /add-media для добавления медиафайлов")
        return embed

    @staticmethod
    def generic_error(message: str = "Произошла ошибка. Пожалуйста, попробуйте позже.") -> Embed:
        return Embed(
            title="❌ Ошибка",
            description=message,
            color=Color.red()
        )