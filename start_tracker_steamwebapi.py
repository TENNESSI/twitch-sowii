import aiohttp
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

STEAM_API_KEY = os.getenv('STEAM_API_KEY')
async def check_current_match(steam_id_64):
    url = f'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={STEAM_API_KEY}&steamids={steam_id_64}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            try:
                data = await response.json(content_type=None)
            except Exception as _e:
                print(f'Ошибка: {_e}')
                data = {}
            players = data.get('response', {}).get('players', [])

            if players:
                player = players[0]
                if player.get('gameid') == '570':
                    return True, player.get('gameserverip', '')
    return False, None

async def track_player(steam_id_64):
    last_status = False

    while True:
        in_match, server_ip = await check_current_match(steam_id_64)

        if in_match and not last_status:
            print(f'Игрок {steam_id_64} начал матч. Сервер: {server_ip}')
            last_status = True
        elif not in_match:
            last_status = False

        await asyncio.sleep(30)
asyncio.run(track_player(os.getenv('steam_id')))