from nextcord.ext.commands import Cog, Bot, command, Context
from nextcord import Embed, Color, Member
from datetime import datetime
import logging
import os
import nextcord

from bot.database import Database
from bot.misc.embeds.projects import ProjectEmbeds
from bot.misc.embeds.media import MediaEmbeds
from bot.misc.embeds.portfolio import PortfolioEmbeds
from bot.misc.media_utils import MediaUtils

logger = logging.getLogger(__name__)


class __ProjectManager(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.db = Database()
        self.media_utils = MediaUtils()

    @command(name="add-project")
    async def add_project(self, ctx: Context, name: str = None, category: str = None, *, description: str = None):
        """Добавить новый проект в портфолио"""
        if any(arg is None for arg in [name, category, description]):
            embed = ProjectEmbeds.add_project_missing_args()
            await ctx.send(embed=embed)
            return

        try:
            # Проверяем количество существующих проектов
            existing_projects = self.db.get_user_projects(ctx.author.id)
            if len(existing_projects) >= 3:
                embed = ProjectEmbeds.project_limit_reached()
                await ctx.send(embed=embed)
                return

            # Проверяем, существует ли уже проект с таким названием
            existing_project = self.db.get_project_by_name(ctx.author.id, name)
            if existing_project:
                embed = ProjectEmbeds.project_exists(name)
                await ctx.send(embed=embed)
                return

            project = self.db.create_project(
                discord_id=ctx.author.id,
                name=name,
                category=category,
                description=description
            )

            remaining = 3 - len(existing_projects) - 1
            embed = ProjectEmbeds.project_added_success(name, category, description, remaining)
            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Ошибка при добавлении проекта: {str(e)}")
            embed = ProjectEmbeds.generic_error("Произошла ошибка при добавлении проекта. Пожалуйста, попробуйте позже.")
            await ctx.send(embed=embed)

    @command(name="add-media")
    async def add_media(self, ctx: Context, project_name: str = None):
        """Добавить медиафайлы к проекту"""
        if project_name is None:
            embed = MediaEmbeds.add_media_missing_args()
            await ctx.send(embed=embed)
            return

        try:
            project = self.db.get_project_by_name(ctx.author.id, project_name)

            if not project:
                embed = ProjectEmbeds.project_exists(project_name)  
                await ctx.send(embed=embed)
                return

            # Проверяем, есть ли вложения в сообщении
            if not ctx.message.attachments:
                embed = MediaEmbeds.no_attachments()
                await ctx.send(embed=embed)
                return

            # Обрабатываем каждое вложение
            added_media = []
            errors = []

            for attachment in ctx.message.attachments:
                try:
                    # Определяем тип медиафайла
                    media_type = MediaUtils.get_media_type(attachment.content_type)
                    if not media_type:
                        errors.append(f"• Неподдерживаемый формат: {attachment.filename}")
                        continue

                    # Скачиваем файл
                    filepath = await self.media_utils.download_media(attachment.url, project.id)
                    # Добавляем запись в базу данных
                    media = self.db.add_media(project.id, filepath, media_type)
                    if media:
                        added_media.append(f"• {attachment.filename}")

                except Exception as e:
                    logger.error(f"Ошибка при обработке медиафайла {attachment.filename}: {str(e)}")
                    errors.append(f"• Ошибка при обработке {attachment.filename}")

            embed = MediaEmbeds.media_add_result(project_name, added_media, errors)
            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Ошибка при добавлении медиафайлов: {str(e)}")
            embed = ProjectEmbeds.generic_error("Произошла ошибка при добавлении медиафайлов. Пожалуйста, попробуйте позже.")
            await ctx.send(embed=embed)

    @command(name="preview")
    async def preview_portfolio(self, ctx: Context, member: Member = None):
        """Предпросмотр портфолио"""
        try:
            target = member or ctx.author
            projects = self.db.get_user_projects(target.id)
            embed = PortfolioEmbeds.portfolio_preview(target, bool(projects))
            await ctx.send(embed=embed)
            if projects:
                for project in projects:
                    project_embed = PortfolioEmbeds.project_details(project)
                    await ctx.send(embed=project_embed)
                    media = self.db.get_project_media(project.id)
                    if media:
                        for m in media:
                            try:
                                if os.path.exists(m.url):
                                    await ctx.send(file=nextcord.File(m.url))
                            except Exception as e:
                                logger.error(f"Ошибка при отправке медиафайла {m.url}: {str(e)}")
                    else:
                        await ctx.send("📎 Нет медиафайлов")
        except Exception as e:
            logger.error(f"Ошибка при загрузке портфолио: {str(e)}")
            embed = ProjectEmbeds.generic_error("Произошла ошибка при загрузке портфолио. Пожалуйста, попробуйте позже.")
            await ctx.send(embed=embed)

    @command(name="remove-media")
    async def remove_media(self, ctx: Context, project_name: str = None):
        """Удалить медиафайлы из проекта"""
        if project_name is None:
            embed = MediaEmbeds.no_media_in_project(project_name or "<не указано>")
            await ctx.send(embed=embed)
            return

        try:
            project = self.db.get_project_by_name(ctx.author.id, project_name)

            if not project:
                embed = ProjectEmbeds.project_exists(project_name)
                await ctx.send(embed=embed)
                return

            media = self.db.get_project_media(project.id)
            if not media:
                embed = MediaEmbeds.no_media_in_project(project_name)
                await ctx.send(embed=embed)
                return

            embed = MediaEmbeds.media_list(project_name, media)
            await ctx.send(embed=embed)

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit()

            try:
                msg = await self.bot.wait_for('message', check=check, timeout=30.0)
                index = int(msg.content) - 1
                if 0 <= index < len(media):
                    file_to_remove = media[index]
                    if os.path.exists(file_to_remove.url):
                        os.remove(file_to_remove.url)
                    with self.db.get_session() as session:
                        session.delete(file_to_remove)
                        session.commit()
                    embed = MediaEmbeds.media_removed(project_name)
                else:
                    embed = ProjectEmbeds.generic_error("Неверный номер файла.")
            except TimeoutError:
                embed = ProjectEmbeds.generic_error("Вы не выбрали файл для удаления.")
            await ctx.send(embed=embed)
        except Exception as e:
            logger.error(f"Ошибка при удалении медиафайла: {str(e)}")
            embed = ProjectEmbeds.generic_error("Произошла ошибка при удалении медиафайла. Пожалуйста, попробуйте позже.")
            await ctx.send(embed=embed)


def register_user_cogs(bot: Bot) -> None:
    bot.add_cog(__ProjectManager(bot)) 