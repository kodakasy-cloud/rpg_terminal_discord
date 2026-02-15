import discord
import random
import os
import asyncio

from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="*", intents=intents)
jogadores = {}

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
             
class PosVitoriaView(discord.ui.View):
    def __init__(self, ctx, jogador):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.jogador = jogador

    @discord.ui.button(label="🌲 Continuar Explorando", style=discord.ButtonStyle.green)
    async def continuar(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.user != self.ctx.author:
            await interaction.response.send_message("Não é seu combate.", ephemeral=True)
            return

        await interaction.response.defer()
        await ExplorarMundo(self.ctx)

    @discord.ui.button(label="👤 Ver Perfil", style=discord.ButtonStyle.blurple)
    async def perfil(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("Não é seu personagem.", ephemeral=True)
            return

        await interaction.response.defer()
        await perfil(self.ctx)

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

class EscolhaClasseView(discord.ui.View):
    def __init__(self, ctx, nome):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.nome = nome

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("Esse personagem não é seu!", ephemeral=True)
            return False
        return True

    def criar_personagem(self, classe):
        jogadores[self.ctx.author.id] = {
            "nome": self.nome,
            "classe": classe["nome"],
            "vida_max": classe["vida"],
            "vida": classe["vida"],
            "energia": 10,
            "level": 1,
            "xp": 0,
            "dinheiro": 0,

            "atk_fisico": classe["atk_fisico"],
            "atk_magico": classe["atk_magico"],
            "def_fisica": classe["def_fisica"],
            "def_magica": classe["def_magica"],
            "agilidade": classe["agilidade"],
            "sorte": classe["sorte"],
            "crit_chance": 0,
            "crit_dano": 0
        }

    @discord.ui.button(label="🗡️ Guerreiro", style=discord.ButtonStyle.red)
    async def guerreiro(self, interaction: discord.Interaction, button: discord.ui.Button):

        classe = {
            "nome": "Guerreiro",
            "vida": 15,
            "atk_fisico": 1,
            "atk_magico": 1,
            "def_fisica": 1,
            "def_magica": 0,
            "agilidade": 0,
            "sorte": 0
        }

        self.criar_personagem(classe)

        await interaction.response.edit_message(
            embed=embed_sucesso(self.ctx, self.nome, "Guerreiro 🗡️"),
            view=None
        )

    @discord.ui.button(label="🔮 Mago", style=discord.ButtonStyle.blurple)
    async def mago(self, interaction: discord.Interaction, button: discord.ui.Button):

        classe = {
            "nome": "Mago",
            "vida": 5,
            "atk_fisico": 0,
            "atk_magico": 3,
            "def_fisica": 0,
            "def_magica": 0,
            "agilidade": 0,
            "sorte": 0
        }

        self.criar_personagem(classe)

        await interaction.response.edit_message(
            embed=embed_sucesso(self.ctx, self.nome, "Mago 🔮"),
            view=None
        )

    @discord.ui.button(label="🏹 Arqueiro", style=discord.ButtonStyle.green)
    async def arqueiro(self, interaction: discord.Interaction, button: discord.ui.Button):

        classe = {
            "nome": "Arqueiro",
            "vida": 5,
            "atk_fisico": 3,
            "atk_magico": 0,
            "def_fisica": 0,
            "def_magica": 0,
            "agilidade": 0,
            "sorte": 0
        }

        self.criar_personagem(classe)

        await interaction.response.edit_message(
            embed=embed_sucesso(self.ctx, self.nome, "Arqueiro 🏹"),
            view=None
        )

class ConfirmarNomeView(discord.ui.View):
    def __init__(self, ctx, nome):
        super().__init__(timeout=30)
        self.ctx = ctx
        self.nome = nome

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("Isso não é para você.", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="✅ Confirmar", style=discord.ButtonStyle.green)
    async def confirmar(self, interaction: discord.Interaction, button: discord.ui.Button):

        embed_classe = discord.Embed(
            title="🧙 Escolha sua Classe",
            description=(
                f"👤 Personagem: **{self.nome}**\n\n"
                "Escolha sua classe inicial:"
            ),
            color=discord.Color.blurple()
        )

        view = EscolhaClasseView(self.ctx, self.nome)

        await interaction.response.edit_message(embed=embed_classe, view=view)

    @discord.ui.button(label="❌ Cancelar", style=discord.ButtonStyle.red)
    async def cancelar(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.edit_message(
            content="❌ Criação cancelada. Use !play novamente.",
            embed=None,
            view=None
        )

class EscolhaClasseView(discord.ui.View):
    def __init__(self, ctx, nome):
        super().__init__(timeout=30)
        self.ctx = ctx
        self.nome = nome
        self.classe = None

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("Isso não é para você.", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="🗡️ Guerreiro", style=discord.ButtonStyle.gray)
    async def guerreiro(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.classe = "Guerreiro"
        await self.confirmar_classe(interaction)

    @discord.ui.button(label="🔮 Mago", style=discord.ButtonStyle.gray)
    async def mago(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.classe = "Mago"
        await self.confirmar_classe(interaction)

    @discord.ui.button(label="🏹 Arqueiro", style=discord.ButtonStyle.gray)
    async def arqueiro(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.classe = "Arqueiro"
        await self.confirmar_classe(interaction)

    async def confirmar_classe(self, interaction):

        embed_confirm = discord.Embed(
            title="⚔ Confirmar Classe",
            description=(
                f"👤 Nome: **{self.nome}**\n"
                f"🎭 Classe: **{self.classe}**\n\n"
                "Deseja confirmar?"
            ),
            color=discord.Color.green()
        )

        view = ConfirmarClasseFinal(self.ctx, self.nome, self.classe)

        await interaction.response.edit_message(embed=embed_confirm, view=view)

class ConfirmarClasseFinal(discord.ui.View):
    def __init__(self, ctx, nome, classe):
        super().__init__(timeout=30)
        self.ctx = ctx
        self.nome = nome
        self.classe = classe

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("Isso não é para você.", ephemeral=True)
            return False
        return True

    # ============================
    # Função para definir atributos base por classe
    # ============================
    def atributos_por_classe(self):

        if self.classe == "Guerreiro":
            return {
                "cor": discord.Color.red(),
                "vida": 15,
                "energia": 0,
                "atk_fisico": 1,
                "atk_magico": 0,
                "def_fisica": 0,
                "def_magica": 0,
                "agilidade": 0,
                "sorte": 0,
                "crit_chance": 0,
                "crit_dano": 0
            }

        elif self.classe == "Mago":
            return {
                "cor": discord.Color.purple(),
                "vida": 8,
                "energia": 0,
                "atk_fisico": 0,
                "atk_magico": 2,
                "def_fisica": 0,
                "def_magica": 0,
                "agilidade": 0,
                "sorte": 0,
                "crit_chance": 0,
                "crit_dano": 0
            }

        elif self.classe == "Assassino":
            return {
                "cor": discord.Color.dark_gray(),
                "vida": 8,
                "energia": 0,
                "atk_fisico": 2,
                "atk_magico": 0,
                "def_fisica": 0,
                "def_magica": 0,
                "agilidade": 0,
                "sorte": 0,
                "crit_chance": 0,
                "crit_dano": 0
            }

        # Classe padrão fallback
        return {
            "cor": discord.Color.green(),
            "vida": 10,
            "energia": 0,
            "atk_fisico": 1,
            "atk_magico": 0,
            "def_fisica": 0,
            "def_magica": 0,
            "agilidade": 0,
            "sorte": 0,
            "crit_chance": 0,
            "crit_dano": 0
        }

    # ============================
    # BOTÃO CONFIRMAR
    # ============================
    @discord.ui.button(label="🔥 Confirmar Classe", style=discord.ButtonStyle.green)
    async def confirmar(self, interaction: discord.Interaction, button: discord.ui.Button):

        atributos = self.atributos_por_classe()

        # Pequena animação fake
        await interaction.response.edit_message(
            embed=discord.Embed(
                title="✨ Canalizando Energia...",
                description=f"Você aceita o caminho do **{self.classe}**...",
                color=atributos["cor"]
            ),
            view=None
        )

        await asyncio.sleep(2)

        # Criando jogador
        jogadores[self.ctx.author.id] = {
            "nome": self.nome,
            "classe": self.classe,
            "vida_max": atributos["vida"],
            "vida": atributos["vida"],
            "energia": atributos["energia"],
            "level": 1,
            "xp": 0,
            "xp_up": 10,
            "dinheiro": 0,
            "atk_fisico": atributos["atk_fisico"],
            "atk_magico": atributos["atk_magico"],
            "def_fisica": atributos["def_fisica"],
            "def_magica": atributos["def_magica"],
            "agilidade": atributos["agilidade"],
            "sorte": atributos["sorte"],
            "crit_chance": atributos["crit_chance"],
            "crit_dano": atributos["crit_dano"]
        }

        embed_final = discord.Embed(
            title="🔥 PERSONAGEM DESPERTADO!",
            description=(
                f"👤 **{self.nome}**\n"
                f"🎭 Classe: **{self.classe}**\n\n"
                "🌲 Você desperta na Floresta Inicial...\n"
                "Seu poder começa a fluir."
            ),
            color=atributos["cor"]
        )

        embed_final.add_field(
            name="📊 Atributos Iniciais",
            value=(
                f"❤️ Vida: {atributos['vida']}\n"
                f"⚡ Energia: {atributos['energia']}\n"
                f"🗡 ATK Físico: {atributos['atk_fisico']}\n"
                f"🔮 ATK Mágico: {atributos['atk_magico']}\n"
                f"🛡 DEF Física: {atributos['def_fisica']}\n"
                f"✨ DEF Mágica: {atributos['def_magica']}\n"
                f"💨 Agilidade: {atributos['agilidade']}\n"
                f"🎲 Sorte: {atributos['sorte']}\n"
                f"💥 Crítico: {atributos['crit_chance']}%"
            ),
            inline=False
        )

        embed_final.set_thumbnail(url=self.ctx.author.display_avatar.url)
        embed_final.set_footer(text="Use *explorar para iniciar sua jornada.")

        await interaction.message.edit(embed=embed_final)

    # ============================
    # BOTÃO VOLTAR
    # ============================
    @discord.ui.button(label="↩ Escolher Outra Classe", style=discord.ButtonStyle.red)
    async def voltar(self, interaction: discord.Interaction, button: discord.ui.Button):

        embed_classe = discord.Embed(
            title="🧙 Escolha sua Classe",
            description=(
                f"👤 Personagem: **{self.nome}**\n\n"
                "Escolha novamente seu caminho."
            ),
            color=discord.Color.blurple()
        )

        view = EscolhaClasseView(self.ctx, self.nome)

        await interaction.response.edit_message(embed=embed_classe, view=view)

def embed_sucesso(ctx, nome, classe_nome):
    embed = discord.Embed(
        title="🔥 Personagem Criado com Sucesso!",
        description=(
            f"👤 Nome: **{nome}**\n"
            f"🧙 Classe: **{classe_nome}**\n"
            f"⭐ Level: 1\n\n"
            "🌲 Você desperta na Floresta Inicial...\n"
            "O ar está pesado.\n"
            "Algo observa você das sombras..."
        ),
        color=discord.Color.gold()
    )

    embed.set_thumbnail(url=ctx.author.display_avatar.url)
    embed.set_footer(text="Use *explorar para iniciar sua aventura.")

    return embed

class CombateView(discord.ui.View):
    def __init__(self, ctx, jogador, inimigo):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.jogador = jogador
        self.inimigo = inimigo
        self.turno = "jogador"

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("Esse combate não é seu!", ephemeral=True)
            return False
        return True

    def criar_embed(self, texto=""):
        embed = discord.Embed(
            title="⚔️ Combate",
            description=texto,
            color=discord.Color.red()
        )

        embed.add_field(
            name=f"👤 {self.jogador['nome']}",
            value=barra_vida(self.jogador["vida"], self.jogador["vida_max"]),
            inline=False
        )

        embed.add_field(
            name=f"🟢 {self.inimigo['nome']}",
            value=barra_vida(self.inimigo["vida"], self.inimigo["vida_max"]),
            inline=False
        )

        embed.set_footer(text=f"Turno: {self.turno.capitalize()}")
        return embed
    

    @discord.ui.button(label="⚔️ Atacar", style=discord.ButtonStyle.red)
    async def atacar(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        if self.turno != "jogador":
            await interaction.response.send_message("Espere seu turno!", ephemeral=True)
            return

        dano = self.jogador["atk_fisico"] or self.jogador["atk_magico"]
        self.inimigo["vida"] -= dano

        texto = f"⚔️ Você causou {dano} de dano!\n"

        if self.inimigo["vida"] <= 0:

            xp_ganho = self.inimigo["xp"]
            ouro_ganho = self.inimigo["dinheiro"]

            drops = []
            for item in self.inimigo.get("drops", []):
                if random.randint(1, 100) <= item["chance"]:
                    drops.append(item["nome"])

            embed = discord.Embed(
                title="🏆 Vitória!",
                description="Derrotando o inimigo...",
                color=discord.Color.green()
            )

            await interaction.response.edit_message(embed=embed, view=None)

            # ---------------- XP ----------------
            await asyncio.sleep(1)

            self.jogador["xp"] += xp_ganho

            embed.add_field(name="✨ XP ganho", value=f"+{xp_ganho}", inline=False)
            await interaction.message.edit(embed=embed)

            # ---------------- Ouro ----------------
            await asyncio.sleep(1)

            self.jogador["dinheiro"] += ouro_ganho

            embed.add_field(name="💰 Ouro ganho", value=f"+{ouro_ganho}", inline=False)
            await interaction.message.edit(embed=embed)

            # ---------------- Drops ----------------
            await asyncio.sleep(1)

            if drops:
                texto_drops = "\n".join([f"🎁 {d}" for d in drops])
            else:
                texto_drops = " Nenhum item encontrado."

            embed.add_field(name="🎁 Itens encontrados", value=texto_drops, inline=False)
            await interaction.message.edit(embed=embed)

            # ---------------- LEVEL UP ----------------
            await asyncio.sleep(1)

            subiu = verificar_xp_up(self.jogador)

            if subiu:
                embed.add_field(
                    name="⬆️ LEVEL UP!",
                    value=f"Agora você é Level {self.jogador['level']}!\n"
                        f"❤️ Vida aumentada!\n"
                        f"⚔️ Ataque aumentado!\n"
                        f"🛡️ Defesa aumentada!",
                    inline=False
                )
                await interaction.message.edit(embed=embed)

            # ---------------- Botões ----------------
            await asyncio.sleep(1)

            view = PosVitoriaView(self.ctx, self.jogador)
            await interaction.message.edit(embed=embed, view=view)

            return



        # Turno do inimigo
        self.turno = "inimigo"

        dano_inimigo = self.inimigo["ataque"]
        self.jogador["vida"] -= dano_inimigo

        texto += f"💢 O {self.inimigo['nome']} causou {dano_inimigo} de dano!"

        if self.jogador["vida"] <= 0:

            self.jogador["vida"] = self.jogador["vida_max"]

            embed = discord.Embed(
                title="☠️ Derrota...",
                description="Você foi derrotado no combate.",
                color=discord.Color.dark_red()
            )

            embed.add_field(
                name="Consequência",
                value="Você perdeu o duelo e voltou para a cidade.",
                inline=False
            )

            await interaction.response.edit_message(embed=embed, view=None)
            return

        # Volta turno
        self.turno = "jogador"

        embed = self.criar_embed(texto)
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="⚔️ Habilidades", style=discord.ButtonStyle.red)
    async def defender(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

    @discord.ui.button(label="⚔️ Analisar", style=discord.ButtonStyle.red)
    async def skils(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

    @discord.ui.button(label="🏃 Correr", style=discord.ButtonStyle.gray)
    async def correr(self, interaction: discord.Interaction, button: discord.ui.Button):

        if self.turno != "jogador":
            await interaction.response.send_message("Espere seu turno!", ephemeral=True)
            return

        chance = random.randint(1, 100)

        if chance <= 40:
            embed = self.criar_embed("🏃 Você fugiu com sucesso!")
            await interaction.response.edit_message(embed=embed, view=None)
        else:
            self.turno = "inimigo"
            dano = self.inimigo["ataque"]
            self.jogador["vida"] -= dano

            embed = self.criar_embed(f"❌ Falhou ao fugir! Recebeu {dano} de dano.")
            self.turno = "jogador"
            await interaction.response.edit_message(embed=embed, view=self)

def barra_vida(atual, maximo, tamanho=10):
    porcentagem = atual / maximo
    blocos = int(porcentagem * tamanho)
    vazios = tamanho - blocos
    barra = "█" * blocos + "░" * vazios
    return f"{barra} {atual}/{maximo}"

def emoji_classe(classe):
    if classe == "Guerreiro":
        return "🗡️"
    elif classe == "Mago":
        return "🔮"
    elif classe == "Arqueiro":
        return "🏹"
    else:
        return "❓"
    
def verificar_xp_up(jogador):
    subiu_level = False

    while True:
        xp_necessario = jogador["level"] * 10

        if jogador["xp"] < xp_necessario:
            break

        jogador["xp"] -= xp_necessario
        jogador["level"] += 1

        jogador["vida_max"] += 2
        jogador["atk_fisico"] += 1
        jogador["def_fisica"] += 1

        jogador["vida"] = jogador["vida_max"]

        subiu_level = True

    return subiu_level

class explorar():

    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @bot.command()
    async def explorar(self, ctx):

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

bot.run("MTQ3MjI2NDQwMTQzMTMwMjE5Ng.Gr35Lt.xcp2_2sVqgVlq9NKTfjk-FJbVEPyGuLKRQX-og")