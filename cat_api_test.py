import requests
from dotenv import load_dotenv
import os
import json

API_KEY = "live_xID7zgqcyR7lDxE0qssvubFHqGX8kJ7w5BHevQNoUh2jpvOU19ORgKX0uJSM3nXQ"
load_dotenv()
api_key = os.getenv("API_KEY")

url = "https://api.thecatapi.com/v1/breeds" 
headers = {"Authorization": f"Bearer {api_key}"}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    data = response.json()
    catlist = []
    for cat in data:
        catlist.append(cat)

else:
    print(f"Error: {response.status_code}, Message: {response.text}")


print(catlist)