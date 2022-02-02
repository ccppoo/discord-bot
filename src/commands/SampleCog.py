from discord.ext.commands.context import Context
from discord.ext import commands
from discord import Message


class SampleCog(commands.Cog):
    
    def __init__(self, bot) -> None:
        self.bot : commands.Bot = bot
        
    # @commands.Cog.listener("on_connect")
    # async def load_database(self):
    #     pass
    
    @commands.Cog.listener("on_ready")
    async def I_am_ready(self):
        print("SampleCog(commands.Cog) ready")
    
    # @commands.Cog.listener("on_message")
    # async def log_messages(self, message : Message):
    #     pass
    
    @commands.command(name="hello", alias=['안녕'])
    async def greetings(self, ctx : Context):
        await ctx.reply(f"{ctx.author.nick} 안녕!")
        
def setup(bot : commands.Bot):
    bot.add_cog(SampleCog(bot))