import discord
from commands.perfil import perfil

class PosVitoriaView(discord.ui.View):
    def __init__(self, ctx, jogador):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.jogador = jogador

    @discord.ui.button(label="🌲 Continuar Explorando", style=discord.ButtonStyle.green)
    async def continuar(self, interaction: discord.Interaction, button: discord.ui.Button):

        from commands.explorar import ExplorarMundo

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