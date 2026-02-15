import discord
from discord.ext import commands
from TESTBOTDISCORD.database.enemy_info import Enemy

permissoes = discord.Intents.default()
permissoes.message_content = True
permissoes.members = True
bot = commands.Bot(command_prefix="*", intents=permissoes)

@bot.event
async def on_ready():
    Enemy()
