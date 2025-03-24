import requests



response = requests.get(
    'https://http://127.0.0.1:5000/quadratic-system'
)

print(response.json())