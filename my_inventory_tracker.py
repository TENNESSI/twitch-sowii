import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread


class GSIServer(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode('utf-8')

        try:
            data = json.loads(body)
            self.handle_data(data)
        except json.JSONDecodeError:
            print('Ошибка декодирования JSON')

        self.send_response(200)
        self.end_headers()

    def handle_data(self, data):
        if 'player' in data and 'items' in data:
            steam_id = data['player'].get('steamid')
            if steam_id:
                items = []
                for slot in [
                    'slot0',
                    'slot1',
                    'slot2',
                    'slot3',
                    'slot4',
                    'slot5',
                    'stash0',
                    'stash1',
                    'stash2',
                    'stash3',
                    'stash4',
                    'stash5',
                ]:
                    item_data = data['items'].get(slot, {})
                    if item_data and 'name' in item_data and item_data['name'] != 'empty':
                        items.append({
                            'slot': slot,
                            'name': item_data['name'],
                            'charges': item_data.get('charges', 0)
                        })

                if steam_id not in self.server.inventory_data:
                    self.server.inventory_data[steam_id] = []
                self.server.inventory_data[steam_id] = items
                print(f'Обновлен инвентарь для {steam_id}: {[item["name"] for item in items]}')

class InventoryTracker:
    def __init__(self, host = 'localhost', port = 3000):
        self.host = host
        self.port = port
        self.server = None
        self.thread = None

    def get_inventory(self, steam_id):
        if self.server and steam_id in self.server.inventory_data:
            return self.server.inventory_data[steam_id]
        return []

    def start(self):
        class CustomHTTPServer(HTTPServer):
            inventory_data = {}

        server_address = (self.host, self.port)
        self.server = CustomHTTPServer(server_address, GSIServer)
        self.thread = Thread(target = self.server.serve_forever())
        self.thread.daemon = True
        self.thread.start()
        print(f'GSI сервер запущен на http://{self.host}:{self.port}')

    def stop(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            if self.thread:
                self.thread.join()
            print('GSI сервер остановлен')

if __name__ == '__main__':
    tracker = InventoryTracker()
    tracker.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        tracker.stop()