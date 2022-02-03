from discord.ext.commands.context import Context
from discord.ext import commands
from ..loader import *
from discord.errors import (
    ExtensionAlreadyLoaded,
    ExtensionNotLoaded,
    NoEntryPointError,
    ExtensionFailed,
    ExtensionNotFound
)

import pathlib, os

__doc__ = '''
BotUtils(commands.Cog)는 커맨드가 작성된 스크립트가 업로드 된 이후로
동적으로 모듈을 리로드하기 위한 디버깅을 위한 Cog 모듈입니다.

AWS 배포를 하면(Github -> ECR -> ECS -> EC2) 로컬에서 즉시 코드를 수정하고 업로드 한 것을 반영할 수 없고,
수정 후 최소 빌드 후 배포까지 평균적으로 3~5 분이 소요됨으로

커맨드 오작동으로 인한 `Cog 언로드`, 이벤트 성으로 잠시 동작하는 커맨드를 위해 `Cog 로드/언로드`, 등등
코드 변경을 반영하기 위한 Cog 모듈 로드 작업은 릴리즈 이후 할 수 없으므로 유의할 것   
'''

EXAMPLE_SETUP_FUNCTION = '''
```py
def setup(bot):
    bot.add_cog(YourCogClass(bot))
```
'''

class BotUtils(commands.Cog):
    
    def __init__(self, bot) -> None:
        self.bot : commands.Bot = bot
        self.__base = 'src'
        self.success_msg = "`성공적으로 {}했습니다!`"
        self.cogs_list = None # will initiate after on_ready

    @commands.Cog.listener("on_ready")
    async def I_am_ready(self, ):
        print("BotUtils(commands.Cog) ready")
        self.__set_cogs()

    def __generate_cog_path(self, cog_name : str) -> str:
        '''
            디버깅을 위해서 cog가 정의된 파이썬 스크립트 경로를 반환해주는 메서드
        '''
        cwd = os.getcwd()
        cog_path = pathlib.Path(os.path.join(cwd, self.__base, *cog_name.split('.')))
        return cog_path

    def __set_cogs(self, ):
        self.cogs_list =['.'.join(x) for x in  [x.split('.')[1:] for x in self.bot.extensions.keys()]]
        print(f"{self.cogs_list=}")

    def __is_dot_py(self, cog_name : str) -> bool:
        '''
            cog 는 파이썬 확장자(`*.py`)를 포함해서 넣는거 아닙니다.
            만약 커맨드로 `.py`를 포함했을 경우를 확인하는 메서드
        '''
        if 'py' in cog_name.split('.'):
            return True
        return False
    
    def __self_examinate(self, cog_name : str) -> str:
        if self.__is_dot_py(cog_name):
            right_name = cog_name.replace('.py', '')
            msg = f"Cog가 정의된 파이썬 스크립트 이름이 `{cog_name}`이라면 `{right_name}`로 보내야 합니다."
            return msg
        
        full_cog_path = self.__generate_cog_path(cog_name)
        msg = f"작성하신 스크립트에 에러가 없는지 확인하세요 : `{full_cog_path}.py`"
        return msg

    '''
    @commands.함수()
        다른 기능들은 아래 링크 참고! : https://gist.github.com/Painezor/eb2519022cd2c907b56624105f94b190
        @commands.is_owner() : 봇 운영자(코드 말고 봇 토큰 주인)만 사용할 수 있도록 제한한 것
    '''
    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def load_cog(self, ctx : Context, *, cog_name : str):
        """
            로드가 `안된` Cog를 로드합니다.
        
            Cog가 src/commands/MyCommands.py 에 정의되었다면
            디스코드 채널에서 아래와 같이 커맨드를 작성하시면됩니다.
            
            `!load commands.MyCommands`
        """
        
        extension_name = '.'.join((self.__base, cog_name))
        
        try:
            self.bot.load_extension(extension_name)
            
        except ExtensionAlreadyLoaded:
            await ctx.send(f'`{cog_name}` 모듈이 이미 로드되어 있습니다')
        
        except ExtensionFailed:
            await ctx.send(f'`{cog_name}` 모듈이 로드 중 에러가 발생했습니다')
        
        except ExtensionNotFound:
            await ctx.send(f'`{cog_name}` 모듈을 찾을 수 없습니다')
        
        except NoEntryPointError:
            full_path = self.__generate_cog_path(cog_name)
            
            msg = f'엔트리 포인트를 찾을 수 없습니다(setup 함수)\n`{full_path}`'
            msg +=f'\n아래와 같은 함수가 정의되어 있는지 확인하길 바랍니다.'
            msg +=f'\n{EXAMPLE_SETUP_FUNCTION}'
            await ctx.send(msg)
            
        except Exception:
            msg = self.__self_examinate(cog_name)
            await ctx.send(msg)
        
        else:
            sm = self.success_msg.format(f"{cog_name} 로드")
            await ctx.send(sm)
        
        finally:
            self.__set_cogs()
        
    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def unload_cog(self, ctx: Context, *, cog_name : str):
        """
            이미 로드되어 있는 Cog를 `언로드`합니다.
        
            Cog가 src/commands/MyCommands.py 에 정의되었다면
            디스코드 채널에서 아래와 같이 커맨드를 작성하시면됩니다.
            
            `!unload commands.MyCommands`
        """
        extension_name = '.'.join((self.__base, cog_name))
        
        try:
            self.bot.unload_extension(extension_name)

        except ExtensionNotFound:
            await ctx.send(f'`{cog_name}` 모듈을 찾을 수 없습니다')

        except ExtensionNotLoaded:
            await ctx.send(f'`{cog_name}` 모듈은 로드되어 있지 않습니다')
        
        except Exception:
            msg = self.__self_examinate(cog_name)
            await ctx.send(msg)
        
        else:
            sm = self.success_msg.format(f"`{cog_name}` 언로드")
            await ctx.send(sm)
        
        finally:
            self.__set_cogs()
        
    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def reload_cog(self, ctx: Context, *, cog_name : str):
        """
            로드되어 있는 Cog를 다시 로드합니다.
            봇을 실행중인 상태에서 파일을 수정후 리로드를 할 수 있으므로 디버깅에 유용합니다.
        
            Cog가 src/commands/MyCommands.py 에 정의되었다면
            디스코드 채널에서 아래와 같이 커맨드를 작성하시면됩니다.
            
            `!reload commands.MyCommands`
        """
        
        extension_name = '.'.join((self.__base, cog_name))
        
        try:
            self.bot.reload_extension(extension_name)
            
        except ExtensionFailed:
            await ctx.send(f'`{cog_name}` 모듈이 로드 중 에러가 발생했습니다')
            
        except ExtensionNotFound:
            await ctx.send(f'`{cog_name}` 모듈을 찾을 수 없습니다')
            
        except ExtensionNotLoaded:
            await ctx.send(f'`{cog_name}` 모듈은 로드되어 있지 않습니다')

        except Exception:
            msg = self.__self_examinate(cog_name)
            await ctx.send(msg)
            
        else:
            sm = self.success_msg.format(f"`{cog_name}` 리로드")
            await ctx.send(sm)
        
        finally:
            self.__set_cogs()
    
    @commands.command(name='cogs', hidden=True)
    @commands.is_owner()
    async def show_cogs(self, ctx: Context):
        cogss = ', '.join([f'`{x}`' for x in self.cogs_list])
        await ctx.reply(cogss)
    
    @commands.command(name='reload-all', hidden=True)
    @commands.is_owner()
    @commands.check(lambda x : False) # 지금은 사용 X -> discord.ext.commands.errors.CheckFailure
    async def reload_all_cog(self, ctx: Context, *, cog_name : str):
        
        cogs = get_commands_cog()
        
        try:
            self.bot.load_extension('.'.join((self.__base, cog_name)))
            self.bot.reload_extension()
            
        except ExtensionAlreadyLoaded:
            await ctx.send(f'`{cog_name}` 모듈이 이미 로드되어 있습니다')
        except ExtensionFailed:
            await ctx.send(f'`{cog_name}` 모듈이 로드 중 에러가 발생했습니다')
        except ExtensionNotFound:
            await ctx.send(f'`{cog_name}` 모듈을 찾을 수 없습니다')
        except ExtensionNotLoaded:
            await ctx.send(f'`{cog_name}` 모듈은 로드되어 있지 않습니다')
        except Exception:
            msg = self.__self_examinate(cog_name)
            await ctx.send(msg)
            
        else:
            sm = self.success_msg.format(f"`{cog_name}` 리로드")
            await ctx.send(sm)
            
        finally:
            self.__set_cogs()
            
def setup(bot : commands.Bot):
    bot.add_cog(BotUtils(bot))