from bot.cogs.user.portfolio_manager import register_user_cogs as register_portfolio
from bot.cogs.user.project_manager import register_user_cogs as register_project
from bot.cogs.user.settings_manager import register_user_cogs as register_settings


def register_user_cogs(bot):
    register_portfolio(bot)
    register_project(bot)
    register_settings(bot)
