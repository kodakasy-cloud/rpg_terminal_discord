import discord
import os
from discord.ext import commands
from view.intro_animada import intro_animada
from view.escolha_classe_view import ConfirmarNomeView

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="k!", intents=intents)
jogadores = {}

async def carregar_cogs():
    for arquivo in os.listdir('commands'):
        if arquivo.endswith('.py'):
            await bot.load_extension(f"commands{arquivo[-3]}")

@bot.command()
async def play(ctx):

    if ctx.author.id in jogadores:
        await ctx.reply("⚠️ Você já possui um personagem criado.")
        return

    mensagem_intro = await intro_animada(ctx)

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for("message", check=check, timeout=30)
        nome = msg.content.strip()

        embed_confirm = discord.Embed(
            title="📜 Confirmar Nome",
            description=f"Seu personagem se chamará:\n\n👤 **{nome}**\n\nDeseja confirmar?",
            color=discord.Color.gold()
        )

        view = ConfirmarNomeView(ctx, nome)

        await ctx.reply(embed=embed_confirm, view=view)

    except:
        await ctx.reply("⏳ Tempo esgotado. Use *play novamente.")

