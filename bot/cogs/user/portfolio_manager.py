from nextcord.ext.commands import Cog, Bot, command, Context

from bot.misc.embeds import other


class __PortfolioManager(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name="start")
    async def start(self, ctx: Context):
        embed = other.get_start_embed()
        
        await ctx.send(embed=embed)

def register_user_cogs(bot: Bot) -> None:
    bot.add_cog(__PortfolioManager(bot))
