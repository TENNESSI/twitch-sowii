# import os
# import asyncio
# from start_tracker import to_steam32
import aiohttp


class StatsProvider:
    def __init__(self):
        self.session = aiohttp.ClientSession()
        self.base_url = 'https://api.opendota.com/api'

    async def get_player_stats(self, account_id):
        url = f'{self.base_url}/players/{account_id}'
        async with self.session.get(url) as response:
            return await response.json()

    async def get_match_stats(self, match_id):
        url = f'{self.base_url}/matches/{match_id}'
        async with self.session.get(url) as response:
            return await response.json()

    async def get_hero_stats(self, hero_id):
        url = f'{self.base_url}/heroes/{hero_id}'
        async with self.session.get(url) as response:
            return await response.json()