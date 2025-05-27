from nextcord import Embed, Color

def get_start_embed() -> Embed:
    """Создает эмбед для команды /start"""
    embed = Embed(
        title="🎨 Добро пожаловать в Portfol.io!",
        description="Создайте своё профессиональное портфолио прямо в Discord.",
        color=Color.blue()
    )
    
    embed.add_field(
        name="📝 Что вы можете сделать:",
        value=(
            "• Добавлять проекты и работы\n"
            "• Загружать изображения и видео\n"
            "• Прикреплять ссылки на внешние ресурсы\n"
            "• Получить готовую веб-страницу портфолио"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🎯 Начните с:",
        value=(
            "`/add-project` - добавить новый проект\n"
            "`/help` - получить список всех команд\n"
            "`/preview` - предпросмотр вашего портфолио"
        ),
        inline=False
    )
    
    embed.set_footer(text="Portfol.io — ваше портфолио в одном сообщении")
    return embed