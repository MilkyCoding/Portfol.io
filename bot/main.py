from nextcord import Intents
from nextcord.ext.commands import Bot

from bot.misc import Env, BotConfig
from bot.cogs import register_all_cogs
from bot.database.models import register_models


def start_bot():
    intents = Intents.default()
    intents.message_content = True

    bot = Bot(BotConfig.CMD_PREFIX, intents=intents)

    bot.remove_command("help")

    register_all_cogs(bot)
    register_models()

    bot.run(Env.TOKEN)
