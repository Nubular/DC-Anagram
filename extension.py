import requests
import json
import websockets
import asyncio
import anagram_solver
import re
import argparse

auth_user = ('nubular', '\\')

header = {
    'Content-Type': 'application/json'
}


class Hub:

    def __init__(self, hub_url):
        self.socket = None
        self.hub_url = hub_url
        self.auth_token = None
        self.auth_header = {"Authorization": self.auth_token,
                            'Content-Type': 'application/json'}
        self.hub_id = None

    async def run(self):
        await self.connect()
        await self.create_session()
        await self.get_hub_id()
        self.populate_info()
        await self.get_stats()
        await  self.chat_event_listener()
        print('listening for chat messages')
        while True:
            resp = await self.socket.recv()
            print(json.loads(resp)['data']['text'])
            if json.loads(resp)['data']['from']['nick'] == '•GamesBot•':
                b = re.search(r'^Question \d+ of \d+\. The word is\:\s(?P<letters>(\w\s)+)',json.loads(resp)['data']['text'])
                if b:
                    print("Question: ",re.sub(r'\s',"",b.group('letters')).lower())
                    words = await anagram_solver.find_words(re.sub(r'\s',"",b.group('letters')).lower())
                    for answer in words: 
                        await self.send_chat(answer)
                        await asyncio.sleep(0.5) #needed ?
                        await self.socket.recv()
                        resp = await self.socket.recv()

                        print(json.loads(resp)['data']['text'])
                        if json.loads(resp)['data']['from']['nick'] == '•GamesBot•':
                            b = re.search(r'^Here is a hint\:',json.loads(resp)['data']['text'])
                            print(b)
                            if b:
                                continue
                            else:
                                break
                        

    async def chat_event_listener(self):
        data = {
            "method": "POST",
            "path": "/hubs/{}/listeners/hub_message".format(self.hub_id),
            "event": "hub_message",
            "id": 1,
            "data": {
                "text": "e",
                "severity": "info"
            }
        }

        await self.socket.send(json.dumps(data))
        


    async def connect(self):
        url = 'ws://localhost:5600/api/v1/'
        self.socket = await websockets.connect(url)

    async def create_session(self):
        # telsu
        data = {
            "method": "POST",
            "path": "/sessions/authorize",
            "callback_id": 1,
            "data": {
                "username": "nubular",
                "password": "\\"
            }
        }

        await self.socket.send(json.dumps(data))
        res = await self.socket.recv()
        self.auth_token = json.loads(res)['data']['auth_token']
        return self.auth_token

    def populate_info(self):
        self.auth_header = {"Authorization": self.auth_token,
                            'Content-Type': 'application/json'}

    async def get_session_info(self):
        data = {
            "method": "GET",
            "path": "/sessions/self",
            "callback_id": 1,
        }
        await self.socket.send(json.dumps(data))
        res = await self.socket.recv()
        print(res)

    async def get_sessions(self):
        data = {
            "method": "GET",
            "path": "/sessions",
            "callback_id": 1,
        }
        await self.socket.send(json.dumps(data))
        res = await self.socket.recv()
        print(res)

    async def get_stats(self):
        data = {
            "method": "GET",
            "path": "/hubs/stats",
            "callback_id": 1,
        }
        await self.socket.send(json.dumps(data))
        res = await self.socket.recv()
        print(res)

    async def send_chat(self, message):
        data = {
            "method": "POST",
            "path": "/hubs/chat_message",
            "callback_id": 1,
            "data": {
                "text": message,
                "hub_urls": [self.hub_url]
            }
        }
        await self.socket.send(json.dumps(data))
        res = await self.socket.recv()
    # Useless
    def recv_chat(self, max_count):
        url = 'http://localhost:5600/api/v1/hubs/{}/messages/{}'.format(
            self.hub_id, max_count)
        data = {
            "method": "GET",
            "path": "/hubs/{}/messages/{}".format(self.hub_id, max_count),
            "callback_id": 1,
        }

        c = requests.get(url, headers=self.auth_header)
        parsed = json.loads(c.text)
        print(json.dumps(parsed, indent=4))

    async def get_hub_id(self):
        data = {
            "method": "POST",
            "path": "/hubs/find_by_url",
            "callback_id": 1,
            "data": {
                "hub_url": self.hub_url
            }
        }
        await self.socket.send(json.dumps(data))
        res = await self.socket.recv()
        self.hub_id = json.loads(res)['data']['id']



async def start(url):
    print("Making Dict")
    anagram_solver.make_dict()
    hub = Hub(url)
    await hub.run()

parser = argparse.ArgumentParser()
parser.add_argument("--url", help="Hub Url", dest="url")

if __name__ == "__main__":
    args = parser.parse_args()
    asyncio.get_event_loop().run_until_complete(start(args.url))