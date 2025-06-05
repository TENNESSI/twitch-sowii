from twitchio.ext import commands
from openai import OpenAI
from config import api_key, twitch_token
import json
import os
import shutil
import random
import logging
import asyncio
import sys


# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger('twitchio')
# logger.setLevel(logging.DEBUG)

# test_users = ['real_anq', 'tinkertwitcher', '']
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

def get_initial_channels():
    with open('settings.json', 'r') as f:
        settings = json.load(f)
    initial_channels = settings[0]['connected_channels']
    print(initial_channels)
    return initial_channels

def get_settings(channel_name, setting_name):
    with open('settings.json', 'r') as f:
        settings = json.load(f)
    for channel in settings[1:]:
        if channel['channel'] == channel_name:
            setting = channel.get(setting_name)
            return setting

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=twitch_token,
            prefix='!',
            initial_channels=get_initial_channels()
        )
    async def event_ready(self):
        print(f'Бот {self.nick} подключен!')

    async def event_message(self, message):
        if message.echo:
            return
        print(f'{message.author.name}: {message.content}')
        channel = self.get_channel(message.channel.name)
        if  message.content.startswith('@ushki_na_makushka'):
            if get_settings(message.channel.name, 'aigirl'):
                if os.path.exists(f'data/{message.author.name}.json') == False:
                    shutil.copy('data/system.json', f'data/{message.author.name}.json')

                with open(f'data/{message.author.name}.json', 'r') as f:
                    messages = json.load(f)
                answer = message.content
                messages.append({'role': 'user', 'content': answer})
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=messages,
                    stream=False
                )
                content = response.choices[0].message.content
                await asyncio.sleep(1.5)
                await channel.send(f'@{message.author.name} {content}')
                messages.append({'role': 'assistant', 'content': content})

                with open(f'data/{message.author.name}.json', 'w') as f:
                    json.dump(messages, f, indent=4)
            else:
                await channel.send(f'Функция отключена на этом канале! (!aigirl)')
        elif message.content.lower() == '!писюнярик':
            if message.author.name == 'dariydoll':
                await channel.send('Дашка ты без пениса, а тот что сзади 27см!!')
            else:
                penis = random.randint(-10,70)
                if penis<1:
                    msg=f'{penis}см, поздравляю у тебя вагина'
                elif penis>50:
                    msg = f'{penis}см, хороший красивый писюнярик, почти как у Ани'
                else:
                    msg = f'{penis}см, средний писюнярик, не впечатлил'
                await asyncio.sleep(1.5)
                await channel.send(f'@{message.author.name}, {msg}')
        await self.handle_commands(message)


    @commands.command()
    async def hello(self, ctx):
        if ctx.author.name == 'tinkertwitcher':
            await asyncio.sleep(1.5)
            await ctx.send(f'Привет, создатель!')
        else:
            await asyncio.sleep(1.5)
            await ctx.send(f'Привет, {ctx.author.name}!')

    @commands.command()
    async def aigirl(self, ctx):
        if ctx.author.name == 'tinkertwitcher':
            with open('settings.json', 'r') as f:
                settings = json.load(f)
            for channel in settings[1:]:
                if channel['channel'] == ctx.channel.name:
                    if not channel['aigirl']:
                        channel['aigirl'] = True
                        await asyncio.sleep(1.5)
                        await ctx.send('Функция включена!')
                    else:
                        channel['aigirl'] = False
                        await asyncio.sleep(1.5)
                        await ctx.send('Функция отключена!')
            with open('settings.json', 'w') as f:
                json.dump(settings, f, indent=4)

if __name__ == '__main__':
    bot= Bot()
    bot.run()