import requests
import json

auth = ('nubular','\\')

header = {
  'Content-Type': 'application/json'
}


def get_stats():
	url = 'http://localhost:5600/api/v1/hubs/stats'
	c = requests.get(url,headers = header, auth = auth)
	print(c.text)

def send_chat(message):
	url = 'http://localhost:5600/api/v1/hubs/chat_message'
	data ={
        "text" : message,
		"third_person" : False,
		"hub_urls": [
			"172.16.48.114"
		]
    }
	c = requests.post(url,headers = header, auth = auth, json = data)
	print(c.text)

def recv_chat(session_id,max_count):
	url = 'http://localhost:5600/api/v1/hubs/{}/messages/{}'.format(session_id,max_count)
	c = requests.get(url,headers = header, auth = auth)
	parsed = json.loads(c.text)
	print(json.dumps(parsed, indent = 4))