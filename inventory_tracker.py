from dota2gsi.server import GameStateServer


class InventoryTracker:
    def __init__(self, port = 3000):
        self.server = GameStateServer(port=port)
        self.server.on('update')(self.handle_update)
        self.player_inventories = {}

    def handle_update(self, state):
        if 'player' in state and 'items' in state:
            steam_id = state['player'].get('steamid')
            if steam_id:
                items = []
                for slot, item_data in state['items'].items():
                    if item_data and 'name' in item_data and item_data['name'] != 'empty':
                        items.append({
                            'slot': slot,
                            'name': item_data['name'],
                            'charges': item_data.get('charges', 0)
                        })

                self.player_inventories[steam_id] = items
                print(f'Обновлен инвентарь для {steam_id}: {[item["name"] for item in items]}')

    def get_inventory(self, steam_id):
        return self.player_inventories.get(steam_id, [])

    def start(self):
        print('Запуск сервера Game State Integration...')
        self.server.start()

if __name__ == '__main__':
    tracker = InventoryTracker()
    tracker.start()

    import time
    while True:
        time.sleep(1)