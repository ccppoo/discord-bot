# 이 예시는 Discord Development Portals에서 'members' 권한 인텐트를 클릭해야 사용할 수 있습니다!
import random

import discord
import asyncio
from discord.message import Message
from discord.ext import commands
from discord.ext.commands.context import Context
from discord.ui import Button, View
from typing import List
import os

TOKEN = os.environ['DISCORD_BOT_TOKEN']

# # 코드가 너무 길어지면 스크립트를 따로 만들어서 import 할 수 있습니다.
# from library import 도서관

# # slash command import
# from slash_commands.library import library_command

description = """Discord Bot 샘플 봇입니다"""

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", description=description, intents=intents)


import threading
import concurrent.futures

concurrent.futures.ThreadPoolExecutor

# library.py 에서 import 한 명령어
# bot.add_command(도서관)
# bot.add_application_command(library_command)

@bot.event
async def on_ready():
    print(f"로그인 성공! 닉네임: {bot.user} 아이디(ID): {bot.user.id}")
    print("------")

@bot.event
async def on_message(message : Message):
    # 이 봇이 작성한 메세지는 무시
    if message.author.id == bot.user.id:
        return
    
    # 다른 봇이 보낸 메시지의 경우 무시
    if message.author.bot:
        return
    
    # 여러분이 만든 서버(길드)만 메세지를 받고 싶다면 이 조건문을 이용하세요
    # 봇을 초대한 서버(길드)이름을 알고 싶다면 print(message.guild.name)를 통해서 확인!
    # if not message.guild.name == "Bot Test":
    #     return
    
    await message.reply(f"{message.author.nick} sent : {message.content}")
    
    # 사용자가 보낸 메세지 객체 - 길드 이름, 유저 이름, 아이디, ... 많은 정보를 가지고 있습니다.
    print(message)
    # 보낸 메세지
    # print(message.content)
    
    # print(f"{message.activity=}")
    # print(f"{message.application=}")
    # print(f"{message.attachments=}")
    # print(f"{message.components=}")
    # print(f"{message.mentions=}")
    # print(f"{message.webhook_id=}")
    # 위에 명시한 command_prefix(명령어 접두어)가 포함된 메세지의 경우
    # 명령을 수행하기 위해 이 코드는 on_message 함수 맨 아래에 작성합니다!
    await bot.process_commands(message)


@bot.command(description="안녕!")
async def hello(ctx : Context):
    import time
    
    time.sleep(5)
    
    button = Button(label="Click me!", style=discord.ButtonStyle.green, emoji="😂")
    view = View()
    view.add_item(button)
    await ctx.send("Hi!", view=view)

"""
람다 비동기 실행

https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.invoke

"""

@bot.command(
    name="dddd",
    description="루프 테스트 2" )
async def run_lambda(ctx : Context):
    await ctx.send(f'starting command dddd')

    def blocking_io():
        # File operations (such as logging) can block the
        # event loop: run them in a thread pool.
        import  time
        try:
            time.sleep(3)
            
            raise Exception("test exception")
        except Exception as e:
            return "Test Exception"
        return 'with 3sec delay ok'
    
    loop = asyncio.get_running_loop()
    await ctx.send(f'get event loop 2')

    ## Options:

    # 1. Run in the default loop's executor:
    result = await loop.run_in_executor(None, blocking_io)
    print('default thread pool', result)
    await ctx.send(f'1) loop.run_in_executor with None 2222')

    # 2. Run in a custom thread pool:
    with concurrent.futures.ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(
            pool, blocking_io)
        print('custom thread pool', result)
    
    await ctx.send(f'2) loop.run_in_executor with ThreadPoolExecutor 2222')


@bot.command(
    name="ssss",
    description="루프 테스트")
async def run_lambda(ctx : Context):
    await ctx.send(f'starting command ssss')
    
    def blocking_io():
        # File operations (such as logging) can block the
        # event loop: run them in a thread pool.
        import time
        try:
            asyncio.sleep(3)
            
            raise Exception("test exception")
        except Exception as e:
            return "Test Exception"
        return 'with 3sec delay ok'
    
    loop = asyncio.get_running_loop()
    await ctx.send(f'get event loop')

    ## Options:

    # 1. Run in the default loop's executor:
    result = await loop.run_in_executor(None, blocking_io)
    print('default thread pool', result)
    await ctx.send(f'1) loop.run_in_executor with None')

    # 2. Run in a custom thread pool:
    with concurrent.futures.ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(
            pool, blocking_io)
        print('custom thread pool', result)
    
    await ctx.send(f'2) loop.run_in_executor with ThreadPoolExecutor')
    
    # await ctx.send(result)
        
    # import boto3
    # lambda_client = boto3.client('lambda')
    # lambda_payload = {'body' : {'data' : 'hello'}}
    
    # response = client.invoke(
    #     FunctionName='string',
    #     InvocationType='Event'|'RequestResponse'|'DryRun',
    #     LogType='None'|'Tail',
    #     ClientContext='string',
    #     Payload=b'bytes'|file,
    #     Qualifier='string'
    # )

    # lambda_client.invoke(FunctionName='myfunctionname', 
    #                     InvocationType='Event',
    #                     Payload=lambda_payload)
    # boto3.invoke()
    
    

@bot.command(description="랜덤으로 골라주기 사용법: !랜덤 하나 둘 셋")
async def 랜덤(ctx : Context, *choices: List[str]):
    """
        choices : List[str]
            사용자가 보낸 명령어를 제외한 메세지
            (위 예시의 경우 ["하나", "둘", "셋"])
            으로 받습니다.
    """
    await ctx.send(random.choice(choices))

@bot.command(description="주어진 초 이후에 알람을 보내드립니다!")
async def 알람(ctx : Context, seconds : str = None):
    """
        seconds : int
            주어진 자연수 만큼 대기 이후 @mention을 통해 알림을 보냅니다.
    """
    if seconds is None:
        await ctx.send(f"몇 초 뒤에 알람을 드릴지 알려주세요!\n사용 예시: !알림 5")
    
    try:
        # 사용자가 입력한 메세지는 str(문자열) 타입으로 들어오기 때문에
        # int(정수형)으로 변환 후 작업을 수행한다.
        seconds = int(seconds)

        await asyncio.sleep(seconds)
        await ctx.send(f"{ctx.author.mention}님 {seconds}초가 지났어요!")
    except Exception as e:
        print(e)
        await ctx.send(f"이건 자연수가 아니자나! {seconds} ")

@bot.command()
async def joined(ctx : Context, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f"{member.name} joined in {member.joined_at}")

bot.run(TOKEN)
