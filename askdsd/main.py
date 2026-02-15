import discord
from discord.ext import commands
from TESTBOTDISCORD.database.enemy_info import Enemy

permissoes = discord.Intents.default()
permissoes.message_content = True
permissoes.members = True
bot = commands.Bot(command_prefix="*", intents=permissoes)

# BOT INICIAR
@bot.event
async def on_ready():
    Enemy()
    
bot.run("MTQ3MjI2NDQwMTQzMTMwMjE5Ng.Gr35Lt.xcp2_2sVqgVlq9NKTfjk-FJbVEPyGuLKRQX-og")