import discord
import random

from discord.ext import commands
from main import intents, bot, jogadores

class ExplorarMundo(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @bot.command()
    async def explorar(self, ctx):

        from view.combate_view import CombateView

        jogador = jogadores.get(ctx.author.id)

        if not jogador:
            await ctx.reply("Você precisa criar personagem com *play")
            return

        inimigo = {
            "nome": "Slime",
            "vida": 5,
            "vida_max": 5,
            "ataque": 2,
            "xp": random.randint(3,5),
            "dinheiro": random.randint(1,3)
        }

        embed = discord.Embed(
            title="🌲 Floresta",
            description="⚠️ Um Slime apareceu!",
            color=discord.Color.green()
        )

        view = CombateView(ctx, jogador, inimigo)

        await ctx.reply(embed=embed, view=view)

    async def setup():
        await bot.add_cog(ExplorarMundo(bot))