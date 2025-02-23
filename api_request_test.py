import requests

base_url = 'http://127.0.0.1:5000/duplicate'

params = {'text':'hello world', 'times': 42, 'case': 'UPPER'}

response = requests.get(base_url, params=params)

print(response.json())
