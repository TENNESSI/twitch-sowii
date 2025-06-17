import os
import asyncio
import aiohttp
from dotenv import load_dotenv

load_dotenv()

STEAM_API_KEY = os.getenv('STEAM_API_KEY')
OPEN_DOTA_API = 'https://api.opendota.com/api'


def to_steam32(steam_id_64):
    return str(int(steam_id_64) - 76561197960265728)


class MatchTracker:
    def __init__(self):
        self.tracked_players = {}
        self.current_matches = {}
        self.session = aiohttp.ClientSession()

    async def add_player(self, steam_id_64):
        self.tracked_players[steam_id_64] = {
            'last_status': None,
            'current_match': None
        }
        print(f'Начато отслеживание игрока {steam_id_64}')

    async def check_player_status(self, steam_id_64):
        try:
            url = f'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={STEAM_API_KEY}&steamids={steam_id_64}'
            async with self.session.get(url) as response:
                print(f'---------\n{url}\n{response.status}\n---------')
                data = await response.json(content_type=None)
                player = data['response']['players'][0]

                if 'gameid' in player and player['gameid'] == '570':
                    opendota_url = f'{OPEN_DOTA_API}/players/{to_steam32(steam_id_64)}/recentMatches'
                    async with self.session.get(opendota_url) as opendota_response:
                        print(f'---------\n{opendota_url}\n{opendota_response.status}\n---------')
                        print(f'Запрос {opendota_url} статус {response.status}')
                        matches = await opendota_response.json(content_type=None)
                        current_match = next((m for m in matches if m['lobby_type'] == 7), None)

                        if current_match:
                            return {
                                'in_game': True,
                                'match_id': current_match['match_id'],
                                'start_time': current_match['start_time']
                            }
            return {'in_game': False}
        except Exception as _e:
            print(f'Ошибка при проверке статуса: {_e}')
            return {'in_game': False}

    async def start_monitoring(self, interval = 60):
        while True:
            for steam_id in list(self.tracked_players.keys()):
                status = await self.check_player_status(steam_id)
                prev_status = self.tracked_players[steam_id]['last_status']

                if status['in_game'] != (prev_status['in_game'] if prev_status else False):
                    if status['in_game']:
                        print(f'Игрок {steam_id} начал матч! ID: {status["match_id"]}')

                    self.tracked_players[steam_id]['last_status'] = status
                    self.tracked_players[steam_id]['current_match'] = status.get('match_id')

            await asyncio.sleep(interval)

async def main():
    tracker = MatchTracker()
    await tracker.add_player(os.getenv('steam_id'))
    await tracker.start_monitoring()

if __name__ == '__main__':
    asyncio.run(main())
