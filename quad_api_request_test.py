import requests



response = requests.get(
    'https://first-api-y6hb.onrender.com/quadratic-system'
)

print(response.json()['quadratic_function'])
print(response.json()['linear_function'])
print(response.json()['factored_function'])
print(response.json()['factors'])
print(response.json()['roots'])
print(response.json()['solutions'])
