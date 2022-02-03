from discord.ext.commands.context import Context
from discord.ext import commands
from discord import Message
from discord.ext.commands.errors import (
    CommandError,
    CommandNotFound,
    CommandOnCooldown,
    CommandInvokeError,
    CommandRegistrationError,
    DisabledCommand
)
import pathlib

__doc__ = '''
`BotLogger(commands.Cog)`는 단순히 로깅을 목적으로 생성되었음.

에러가 발생해 호출 된 메서드(예: `on_command_error`) 내부에서 다시 에러가 발생하면
핸들링 되지 못하고, 이벤트 루프가 멈출 수 있으므로 방어적으로 코드를 작성할 것.
(자신 없으면 `try + except` 떡칠하세요)

로깅을 위한 Cog이므로 `ctx : Context`를 이용해 채널/길드에 개입하는 일을 최대한 자제할 것
(예 : 치명적 단계의 로그의 경우 알림 용도로 채널 전송 ok, 디버깅 용도로 ctx.send(...) **NO** )

로컬 환경에서는 sqlite를 이용, DISCORD-BOT/logs 에 저장됨
AWS 상에서 호스팅을 하는 상황에서는 AWS RDS에 I/O 작업을 진행할 예정

아래 함수들은 직접 호출되는 것이 아닌, 이벤트가 발생할 때 호출됨

`on_ ...`으로 시작하는 이벤트는 아래에서 참고!
https://docs.pycord.dev/en/master/api.html?highlight=view#event-reference
https://docs.pycord.dev/en/master/ext/commands/api.html?highlight=on_command#event-reference

예시)
    `on_ready`      : 봇이 최종적으로 준비 완료할 때 발생하는 이벤트
    `on_message`    : 길드-채널, 개인 메세지(private message)에서 메세지를 수신할 때 발생하는 이벤트
    `on_error`      : 에러가 발생할 때 발생하는 이벤트
'''

# FIXME : ctx.reply -> logging.[ .. ] 로깅 함수로 바꾸기 / 선택에 따라서 테스트용 서버의 경우 채널에 메세지 보내는 옵션도 넣기

class BotLogger(commands.Cog):
    
    def __init__(self, bot) -> None:
        self.bot : commands.Bot = bot
    
    @commands.Cog.listener("on_connect")
    async def load_database(self):
        pass
    
    @commands.Cog.listener("on_ready")
    async def I_am_ready(self):
        print("BotLogger(commands.Cog) ready")
    
    @commands.Cog.listener("on_message")
    async def log_messages(self, message : Message):
        pass
    
    @commands.Cog.listener("on_command")
    async def on_command(self, ctx: Context):
        print(f'on_command invoked Cog : {ctx.cog.__module__}')

    @commands.Cog.listener("on_command_error")
    async def on_command_error(self, ctx : Context, exception : Exception):
        
        # TODO : fill with usefull error message
        
        if not isinstance(exception, CommandError):
            # This should not happen
            return await ctx.send(exception)
        
        if isinstance(exception, CommandNotFound):
            err_msg = "on_command_error :: CommandNotFound\n"
            err_msg += f"`{exception}`"
            await ctx.send(err_msg)
        
        if isinstance(exception, CommandInvokeError):
            cog_path = (ctx.cog.__module__).replace('.', '/')
            err_msg = "on_command_error :: CommandInvokeError\n"
            err_msg += f"`{exception}`\n"
            err_msg += f"Error from : `{pathlib.Path(cog_path)}`"
            await ctx.send(err_msg)
        
        if isinstance(exception, CommandOnCooldown):
            await ctx.send(exception)
        
        if isinstance(exception, CommandRegistrationError):
            await ctx.send(exception)
        
        if isinstance(exception, DisabledCommand):
            await ctx.send(exception)
        
        print(f"{exception=}")
        
        
    @commands.Cog.listener("on_command_completion")
    async def on_command_completion(self, ctx : Context):
        # TODO : split command error cases and add message for debuging
        pass
    
    @commands.Cog.listener("on_application_command_error")
    async def on_application_command_error(self, ctx : Context, exception : Exception):
        cog_path = (ctx.cog.__module__).replace('.', '/')
        err_msg = "on_application_command_error\n"
        err_msg += f"`{exception}`"
        err_msg += f"Error at : `{pathlib.Path(cog_path)}`"
        await ctx.send(err_msg)
    
def setup(bot : commands.Bot):
    bot.add_cog(BotLogger(bot))