import discord

from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="*", intents=intents)
jogadores = {}

@bot.command()
async def ranks(ctx):

    if not jogadores:
        await ctx.reply("Nenhum jogador registrado ainda.")
        return

    embed = discord.Embed(
        title="🏆 Ranking Global",
        description="Os jogadores mais fortes do mundo 🌎",
        color=discord.Color.gold()
    )

    # ==============================
    # Medalhas
    # ==============================
    def medalha(pos):
        return ["🥇", "🥈", "🥉", "🏅", "🏅"][pos-1] if pos <= 5 else "🏅"

    # ==============================
    # Emoji Classe
    # ==============================
    def emoji_classe(classe):
        if classe == "Guerreiro":
            return "🗡️"
        elif classe == "Mago":
            return "🔮"
        elif classe == "Arqueiro":
            return "🏹"
        else:
            return "❓"

    # ==============================
    # Calcular Poder
    # ==============================
    def calcular_poder(dados):
        atributos = [
            "atk_fisico",
            "atk_magico",
            "def_fisica",
            "def_magica",
            "agilidade",
            "sorte",
            "crit_chance",
            "crit_dano",
            "level"
        ]
        return sum(dados.get(attr, 0) for attr in atributos)

    # ==============================
    # ⭐ Ranking por LEVEL
    # ==============================
    ranking_level = sorted(
        jogadores.items(),
        key=lambda item: item[1]["level"],
        reverse=True
    )

    texto_level = ""
    for pos, (user_id, dados) in enumerate(ranking_level[:5], start=1):
        classe = dados.get("classe", "Desconhecido")
        texto_level += (
            f"{medalha(pos)} "
            f"{emoji_classe(classe)} "
            f"{dados['nome']} "
            f"({classe}) — Lv {dados['level']}\n"
        )

    texto_level = f"```{texto_level or 'Sem dados'}```"

    # ==============================
    # 💰 Ranking por DINHEIRO
    # ==============================
    ranking_dinheiro = sorted(
        jogadores.items(),
        key=lambda item: item[1]["dinheiro"],
        reverse=True
    )

    texto_dinheiro = ""
    for pos, (user_id, dados) in enumerate(ranking_dinheiro[:5], start=1):
        classe = dados.get("classe", "Desconhecido")
        texto_dinheiro += (
            f"{medalha(pos)} "
            f"{emoji_classe(classe)} "
            f"{dados['nome']} "
            f"({classe}) — ${dados['dinheiro']}\n"
        )

    texto_dinheiro = f"```{texto_dinheiro or 'Sem dados'}```"

    # ==============================
    # ⚔ Ranking por PODER TOTAL
    # ==============================
    ranking_poder = sorted(
        jogadores.items(),
        key=lambda item: calcular_poder(item[1]),
        reverse=True
    )

    texto_poder = ""
    for pos, (user_id, dados) in enumerate(ranking_poder[:5], start=1):
        classe = dados.get("classe", "Desconhecido")
        poder = calcular_poder(dados)
        texto_poder += (
            f"{medalha(pos)} "
            f"{emoji_classe(classe)} "
            f"{dados['nome']} "
            f"({classe}) — {poder} ⚔\n"
        )

    texto_poder = f"```{texto_poder or 'Sem dados'}```"

    # ==============================
    # Adicionando no Embed
    # ==============================
    embed.add_field(name="⭐ Ranking por Level", value=texto_level, inline=False)
    embed.add_field(name="💰 Ranking por Dinheiro", value=texto_dinheiro, inline=False)
    embed.add_field(name="⚔ Ranking por Poder Total", value=texto_poder, inline=False)

    embed.set_footer(text="Top 5 jogadores • Atualizado em tempo real")

    await ctx.reply(embed=embed)