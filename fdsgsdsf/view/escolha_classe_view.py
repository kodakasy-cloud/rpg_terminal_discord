import discord
import asyncio

from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="*", intents=intents)
jogadores = {}

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