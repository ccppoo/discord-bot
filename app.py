import discord
from discord.ext import commands
from src.loader import *
from setup import *

description = """K-Net 디스코드 봇 입니다!"""

intents = discord.Intents.default()
intents.members = True

# prefix는 여러개 할 수 있지만, 특정 prefix를 기준으로 특정 커맨드만 그룹으로 묶는 경우는 on_message로 구분해야함
bot = commands.Bot(
        command_prefix=["!", "?"], 
        description=description, 
        intents=intents, 
        strip_after_prefix=False)

for cog in get_utils_cog():
    bot.load_extension(cog)

for cog in get_commands_cog():
    bot.load_extension(cog)

bot.run(TOKEN)

# comment