import discord
import asyncio

async def intro_animada(ctx):

    mensagem = await ctx.reply("🌑 .")

    await asyncio.sleep(0,1)
    await mensagem.edit(content="🌑 . .")

    await asyncio.sleep(0,1)
    await mensagem.edit(content="🌑 . . .")

    await asyncio.sleep(0,1)

    embed1 = discord.Embed(
        title="🌑 Escuridão...",
        description="Você abre os olhos lentamente.",
        color=discord.Color.dark_gray()
    )
    await mensagem.edit(content=None, embed=embed1)

    await asyncio.sleep(0,1)

    embed2 = discord.Embed(
        title="🌲 Floresta Desconhecida",
        description=(
            "O vento sopra entre as árvores...\n"
            "Algo parece estar observando você."
        ),
        color=discord.Color.dark_green()
    )
    await mensagem.edit(embed=embed2)

    await asyncio.sleep(0,1)

    embed3 = discord.Embed(
        title="👁 Presença Detectada",
        description="Uma energia estranha percorre seu corpo...",
        color=discord.Color.red()
    )
    await mensagem.edit(embed=embed3)

    await asyncio.sleep(0,1)

    embed4 = discord.Embed(
        title="⚔ Seu destino começa agora.",
        description="Digite o nome do seu personagem.",
        color=discord.Color.gold()
    )
    embed4.set_footer(text="Você tem 30 segundos para responder.")
    await mensagem.edit(embed=embed4)

    return mensagem