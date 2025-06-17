import logging
from dota2gsipy.server import GSIServer
import os

logging.basicConfig(level=logging.INFO)

server=GSIServer(("127.0.0.1", 4000),os.getenv('STEAM_API_KEY'))
server.start_server()

while True:
    print(f'Gold: {server.game_state.player.gold}')
    print(f'Name: {server.game_state.player.name}')
    print(f'Hero name: {server.game_state.hero.name}')
    print(f'Pos: {server.game_state.hero.pos}')
    print(f'Talents: {server.game_state.hero.talents}')