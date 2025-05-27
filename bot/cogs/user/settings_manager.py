from nextcord.ext.commands import Cog, Bot, command, Context, CommandNotFound
from nextcord import Member
import logging
from typing import Optional, Tuple, List

from bot.database import Database
from bot.database.models import Link
from bot.misc.embeds.projects import ProjectEmbeds
from bot.misc.embeds.media import MediaEmbeds
from bot.misc.embeds.profile import ProfileEmbeds

logger = logging.getLogger(__name__)


class __SettingsManager(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.db = Database()

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error):
        """Обработка ошибок команд"""
        if isinstance(error, CommandNotFound):
            await ctx.send(embed=ProjectEmbeds.generic_error(
                "Такой команды не существует.\nИспользуйте `/help` для просмотра списка доступных команд."
            ))
            return

        logger.error(f"Ошибка при выполнении команды: {str(error)}")
        await ctx.send(embed=ProjectEmbeds.generic_error())

    async def _handle_error(self, ctx: Context, error: Exception, action: str):
        """Обработка ошибок с логированием"""
        logger.error(f"Ошибка при {action}: {str(error)}")
        await ctx.send(embed=ProjectEmbeds.generic_error(
            f"Произошла ошибка при {action}. Пожалуйста, попробуйте позже."
        ))

    @command(name="profile")
    async def view_profile(self, ctx: Context, member: Optional[Member] = None):
        """Просмотр профиля пользователя"""
        try:
            target = member or ctx.author
            user = self.db.get_user(target.id)
            
            if not user:
                await ctx.send(embed=ProjectEmbeds.generic_error(
                    f"Профиль пользователя {target.mention} не найден."
                ))
                return

            links = self.db.get_user_links(target.id)
            await ctx.send(embed=ProfileEmbeds.profile_view(
                member=target,
                bio=user.bio,
                links=links,
                is_own_profile=(target.id == ctx.author.id)
            ))

        except Exception as e:
            await self._handle_error(ctx, e, "просмотре профиля")

    @command(name="set-profile")
    async def set_profile(self, ctx: Context, *, bio: Optional[str] = None):
        """Установить описание профиля"""
        if bio is None:
            await ctx.send(embed=ProjectEmbeds.generic_error(
                "Пожалуйста, укажите описание профиля.\nПример: `/set-profile Я веб-разработчик с 5-летним опытом...`"
            ))
            return

        try:
            self.db.update_user_bio(ctx.author.id, bio)
            await ctx.send(embed=ProfileEmbeds.profile_updated(bio))

        except Exception as e:
            await self._handle_error(ctx, e, "обновлении профиля")

    def _parse_links(self, links: str) -> Tuple[List[Tuple[str, str]], List[str]]:
        """Парсинг ссылок из строки"""
        parsed_links = []
        errors = []

        for pair in (pair.strip() for pair in links.split(",")):
            try:
                title, url = pair.split(":", 1)
                title, url = title.strip(), url.strip()

                if not url.startswith(("http://", "https://")):
                    url = "https://" + url

                parsed_links.append((url, title))

            except ValueError:
                errors.append(f"• Неверный формат: {pair}")

        return parsed_links, errors

    @command(name="set-links")
    async def set_links(self, ctx: Context, *, links: Optional[str] = None):
        """Установить внешние ссылки"""
        if links is None:
            await ctx.send(embed=ProjectEmbeds.generic_error(
                "Пожалуйста, укажите ссылки в формате:\n"
                "`/set-links Название: URL, Название: URL`\n\n"
                "Пример:\n"
                "`/set-links GitHub: https://github.com/username, LinkedIn: https://linkedin.com/in/username`"
            ))
            return

        try:
            parsed_links, errors = self._parse_links(links)

            if parsed_links:
                self.db.set_links(ctx.author.id, parsed_links)

            added_links = [f"• {title}: {url}" for url, title in parsed_links]
            await ctx.send(embed=ProfileEmbeds.links_updated(added_links, errors))

        except Exception as e:
            await self._handle_error(ctx, e, "обновлении ссылок")

    @command(name="help")
    async def help_command(self, ctx: Context):
        """Показать список доступных команд"""
        await ctx.send(embed=ProfileEmbeds.help_command())


def register_user_cogs(bot: Bot) -> None:
    bot.add_cog(__SettingsManager(bot)) 