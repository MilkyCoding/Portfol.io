from nextcord import Embed, Color, Member

class PortfolioEmbeds:
    @staticmethod
    def portfolio_preview(member: Member, has_projects: bool) -> Embed:
        embed = Embed(
            title=f"👁️ Портфолио {member.display_name}",
            description="Список проектов:",
            color=Color.blue()
        )

        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)
        
        if not has_projects:
            embed.add_field(
                name="Проекты",
                value="У пользователя пока нет добавленных проектов.",
                inline=False
            )

        return embed

    @staticmethod
    def project_details(project) -> Embed:
        return Embed(
            title=f"📁 {project.name}",
            description=(
                f"**Категория:** {project.category}\n"
                f"**Описание:** {project.description}"
            ),
            color=Color.blue()
        )