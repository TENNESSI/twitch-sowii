from twitchio.ext import commands
from openai import OpenAI
from config import api_key, twitch_token
import json
import os
import shutil

test_users = ['real_anq', 'ovcesobaka', 'tinkertwitcher']
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=twitch_token,
            prefix='!',
            initial_channels=['real_anq', 'sowiiaxi_', 'mandellshtam']
        )
    async def event_ready(self):
        print(f'Бот {self.nick} подключен!')

    async def event_message(self, message):
        if message.echo:
            return
        print(f'{message.author.name}: {message.content}')

        if message.author.name in test_users and message.content.startswith('@tinkertwitcher'):
            channel = self.get_channel(message.channel.name)
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
            await channel.send(f'@{message.author.name} {content}')
            messages.append({'role': 'assistant', 'content': content})

            with open(f'data/{message.author.name}.json', 'w') as f:
                json.dump(messages, f, indent=4)

        await self.handle_commands(message)

    @commands.command()
    async def test(self, ctx):
        if ctx.author.name == 'tinkertwitcher':
            await ctx.send(f'Привет, создатель!')
        else:
            await ctx.send(f'Привет, {ctx.author.name}!')

if __name__ == '__main__':
    bot= Bot()
    bot.run()