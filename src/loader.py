from typing import List, Optional
import pathlib, os

__all__ = [
    "get_utils_cog",
    "get_commands_cog"
]

def get_utils_cog() -> List[str]:
    '''
    discord-bot/src/utils 폴더 내부 `*.py`를 불러옵니다.
    
    `*.py` 내부에는 discord.ext.commands.Cog 클래스를 상속한 서브 클래스와
    setup 함수가 정의되어 있어야합니다.
    '''
    bot_utils = pathlib.Path(os.path.join(os.getcwd(), 'src', 'utils'))

    cog_names = []

    for name in os.listdir(bot_utils):
        # Cog 파일이 아닌, 유틸성 함수만 있는 경우
        if name == name.lower():
            continue
        
        if not os.path.isfile(os.path.join(bot_utils, name)):
            continue
        
        if name.endswith('.py'):
            module_name = os.path.basename(name)[:-3]
            cog_name = '.'.join(('src', 'utils', module_name))
            cog_names.append(cog_name)

    return cog_names

def get_commands_cog(*dir : Optional[List[str]] ) -> List[str]:
    '''
    기본값 : `discord-bot/src/commands` 폴더 내부 `*.py` 모듈을 불러옵니다.
    
    `*.py` 내부에는 discord.ext.commands.Cog 클래스를 상속한 서브 클래스와
    setup 함수가 정의되어 있어야합니다.
    
    `discord-bot/src/commands` 폴더가 아닌 다른 위치에 있는 커맨드의 경우
    
    예) discord-bot/src/slash_commands/sample
    
        `get_commands_cog('slash_commands', 'sample')`와 같이 사용하면 됩니다.
    '''
    
    if not dir:
        dir =  ['commands']
    
    cogdir = pathlib.Path(os.path.join(os.getcwd(), 'src', *dir))
    
    cog_names = []
    
    for name in os.listdir(cogdir):
        # Cog 클래스가 정의된 아닌 파일은 반드시 소문자로만 작성
        if name != name.lower():
            continue
        
        if not os.path.isfile(os.path.join(cogdir, name)):
            continue
        
        if name.endswith('.py'):
            module_name = os.path.basename(name)[:-3]
            cog_name = '.'.join(('src', *dir, module_name))
            cog_names.append(cog_name)

    return cog_names