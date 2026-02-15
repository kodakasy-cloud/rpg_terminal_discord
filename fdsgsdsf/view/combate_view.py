import discord
import random
import asyncio
from systems.verificacao_xp_up import verificar_xp_up

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

        from view.pos_vitoria_view import PosVitoriaView
        
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