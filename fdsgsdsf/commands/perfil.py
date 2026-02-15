import discord

from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="*", intents=intents)
jogadores = {}

@bot.command()
async def perfil(ctx):

    if ctx.author.id not in jogadores:
        await ctx.reply("Você ainda não tem um personagem! Use *play.")
        return

    jogador = jogadores[ctx.author.id]

    # =============================
    # 🎨 Cor dinâmica baseada no level
    # =============================
    level = jogador["level"]

    if level <= 3:
        cor = discord.Color.green()
        rank = "🟢 Iniciante"
    elif level <= 5:
        cor = discord.Color.blue()
        rank = "🔵 Aventureiro"
    elif level <= 10:
        cor = discord.Color.purple()
        rank = "🟣 Veterano"
    else:
        cor = discord.Color.gold()
        rank = "🟡 Lendário"

    # =============================
    # 📊 Sistema novo de XP
    # =============================
    xp = jogador["xp"]
    xp_max = jogador["level"] * 10  # <- mesmo cálculo do level up

    porcentagem = xp / xp_max if xp_max > 0 else 0
    blocos = int(porcentagem * 10)

    barra = "🟩" * blocos + "⬛" * (10 - blocos)
    porcento_txt = int(porcentagem * 100)

    # =============================
    # 🧱 Criando Embed
    # =============================
    embed = discord.Embed(
        title=f"👤 Perfil de {jogador['nome']}",
        description=f"🏷 Rank: **{rank}**",
        color=cor
    )

    embed.set_thumbnail(url=ctx.author.display_avatar.url)

    # =============================
    # 🧍 Informações principais
    # =============================
    embed.add_field(
        name="🧍 Status Principal",
        value=(
            f"⭐ Level: **{jogador['level']}**\n"
            f"❤️ Vida: **{jogador['vida']} / {jogador['vida_max']}**\n"
            f"⚡ Energia: **{jogador['energia']}**\n"
            f"💰 Dinheiro: **{jogador['dinheiro']}**"
        ),
        inline=True
    )

    # =============================
    # 📈 XP
    # =============================
    embed.add_field(
        name="✨ Experiência",
        value=(
            f"`{barra}` {porcento_txt}%\n"
            f"{xp} / {xp_max} XP"
        ),
        inline=True
    )

    # =============================
    # ⚔ Atributos
    # =============================
    embed.add_field(
        name="⚔ Atributos de Combate",
        value=(
            f"🗡 ATK Físico: {jogador['atk_fisico']}\n"
            f"🔮 ATK Mágico: {jogador.get('atk_magico', 0)}\n"
            f"🛡 DEF Física: {jogador['def_fisica']}\n"
            f"✨ DEF Mágica: {jogador.get('def_magica', 0)}"
        ),
        inline=False
    )

    embed.add_field(
        name="🍀 Atributos Extras",
        value=(
            f"💨 Agilidade: {jogador.get('agilidade', 0)}\n"
            f"🎲 Sorte: {jogador.get('sorte', 0)}\n"
            f"💥 Chance Crítica: {jogador.get('crit_chance', 0)}%\n"
            f"🔥 Dano Crítico: {jogador.get('crit_dano', 0)}%"
        ),
        inline=False
    )

    embed.set_footer(text="RPG DOIDO • Versão 0.01 ⚔️")

    await ctx.reply(embed=embed)