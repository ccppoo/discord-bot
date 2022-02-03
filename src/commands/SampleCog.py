from discord.ext.commands.context import Context
from discord.ext import commands
from discord import Message


class SampleCog(commands.Cog):
    
    def __init__(self, bot) -> None:
        self.bot : commands.Bot = bot
    
    @commands.Cog.listener("on_ready")
    async def I_am_ready(self):
        print("SampleCog(commands.Cog) ready")
    
    @commands.Cog.listener("on_message")
    async def mirror(self, message : Message):
        pass
    
    @commands.command(name="ping", aliases= ["핑"])
    async def ping(self, ctx : Context):
        await ctx.reply(f"Pong! {self.bot.latency:.2f} ms")

    @ping.error
    async def on_error(self, ctx : Context, exception : Exception):
        await ctx.reply(f"이런! Ping 할 수 없군요! : `{exception}`")

    @commands.command(name="hello", aliases=['안녕'])
    async def greetings(self, ctx : Context):
        await ctx.reply(f"{ctx.author.nick} 안녕!")
    
    @greetings.error
    async def on_error(self, ctx : Context, exception : Exception):
        await ctx.reply(f"이런! 안녕 할 수 없군요! : `{exception}`")
    
def setup(bot : commands.Bot):
    bot.add_cog(SampleCog(bot))