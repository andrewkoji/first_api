import requests

base_url = 'https://first-api-y6hb.onrender.com/chatbot'

params = {'prompt':'explain the history of coding and hello world'}

response = requests.get(base_url, params=params)

print(response.json())
