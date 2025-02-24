import requests

base_url = 'https://first-api-y6hb.onrender.com/lowercase'

params = {'text':'summarize this email: After seeing that Williamsville is no. 1 rated school district: Another strategy is to buy a starter home in Williamsville. Yes smaller in size, but mortgage would be less and upside for value could be good enough to resell with ease at a profit. Also have lower mortgage payment. also money available for small renovations. Downside: house size for ones I found is ca 2000 sq feet (like our house). Know nothing about addresses, but they look ok. You might have to think of probably three bedrooms (ok while you have one child of course, but dont have twins!).'}

response = requests.get(base_url, params=params)

print(response.json())
