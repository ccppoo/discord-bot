from discord.ext.commands.context import Context
from discord.ext.commands.errors import *
from discord.ext import commands
from discord import Message

__doc__ = """
커맨드 에러를 핸들링하는 Cog

모든 커맨드는 아래에 작성했듯, 반드시 `@<함수 이름>.error`와 같이 반드시 에러를 핸들링 할 수 있도록 한다.

이 Cog는 에러를 로깅하는 용도가 아니라, 커버링되지 못한 함수를 커버하고(임시 방편)

봇을 운영하면서 프론트(커맨드, 상호작용)와 봇 클라이언트(내부 로직 에러) Fail 횟수를 기록하는 등

운용에 있어서 10분 당 Fail 횟수 임계치 넘어서면 보고 or 위험한 접근(suspicious attempt) 감시 용도로 사용된다.


반드시 모든 커맨드를 작성할 때, 커맨드의 에러를 핸들링할 수 있는 함수를 작성해야한다.
아래 참고!
https://docs.pycord.dev/en/master/ext/commands/commands.html#error-handling

```py
@bot.command()
async def info(ctx, *, member: discord.Member):
    msg = f'{member} joined on {member.joined_at} and has {len(member.roles)} roles.'
    await ctx.send(msg)

@info.error -> 이렇게 커맨드 @<메서드 이름>.error 데코레이터를 작성해 에러를 처리해야한다.
async def info_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('I could not find that member...')
```

이미 정의한 커맨드 에러를 핸들링하고(사용자가 커맨드 이름 제대로 작성했을 경우)
그 외에 commands.error의 경우 `BotWatcher` Cog가 에러를 핸들링한다.
(예: 존재하지 않는 커맨드를 사용했을 경우, 미처 처리하지 못한 핸들링의 경우)

@commands.command()로 인해서 발생할 수 있는 예외(Exceptions)는 아래 링크 참고:
https://docs.pycord.dev/en/master/ext/commands/api.html#exceptions
"""

class BotWatcher(commands.Cog):
    
    def __init__(self, bot) -> None:
        self.bot : commands.Bot = bot
        
    
def setup(bot : commands.Bot):
    bot.add_cog(BotWatcher(bot))