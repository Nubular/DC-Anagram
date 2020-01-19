import requests
import json

auth_user = ('nubular','\\')

header = {
  'Content-Type': 'application/json'
}

class Hub:

	def __init__(self,hub_url):
		self.hub_url = hub_url
		self.auth_token = self.create_session()
		self.auth_header = {
			"Authorization": self.auth_token,
			'Content-Type': 'application/json'
			}		
		self.hub_id = self.get_hub_id(self.hub_url)


	def create_session(self):
		#telsu
		data = {
			"username" : "nubular",
			"password" : "\\",
			"max_inactivity": 60
		}
		url = 'http://localhost:5600/api/v1/sessions/authorize'
		c = requests.post(url,headers = header, json = data).json()
		try:
			return c['auth_token']
		except:
			print(c)
	def create_socket(self):
		url = 'http://localhost:5600/api/v1/sessions/socket'
		data = {
			"auth_token" : self.auth_token
		}
		c = requests.post(url,headers = header, json = data).json()
		print(c)


	def get_session_info(self):
		url = 'http://localhost:5600/api/v1/sessions/self'
		c = requests.get(url,headers = self.auth_header).json()
		print(c)

	def get_sessions(self):
		url = 'http://localhost:5600/api/v1/sessions'
		c = requests.get(url,headers = self.auth_header).json()
		print(c)

	def get_stats(self):
		url = 'http://localhost:5600/api/v1/hubs/stats'
		c = requests.get(url,headers = self.auth_header)
		parsed = json.loads(c.text)
		print(json.dumps(parsed, indent = 4))

	def send_chat(self,message):
		url = 'http://localhost:5600/api/v1/hubs/chat_message'
		data ={
			"text" : message,
			"third_person" : False,
			"hub_urls": [
				"172.16.48.114"
			]
		}
		c = requests.post(url,headers = self.auth_header, json = data)
		print(c.text)

	def recv_chat(self,max_count):
		url = 'http://localhost:5600/api/v1/hubs/{}/messages/{}'.format(self.hub_id,max_count)
		c = requests.get(url,headers = self.auth_header)
		parsed = json.loads(c.text)
		print(json.dumps(parsed, indent = 4))

	def get_hub_id(self,hub_url):
		url = 'http://localhost:5600/api/v1/hubs/find_by_url'
		data = {
			"hub_url" : hub_url
		}
		c = requests.post(url,headers = self.auth_header, json = data).json()
		return c['id']
	
	def message_event_listener(self):
		url = 'http://localhost:5600/api/v1/hubs/{}/listeners/hub_message'.format(self.hub_id)
		c = requests.post(url,headers = self.auth_header)
		print(c.text)
