import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    print("❌ GOOGLE_API_KEY not found in .env file.")
    exit()

def search_google_places(query, location):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": f"{query} in {location}",
        "key": API_KEY
    }

    res = requests.get(url, params=params)
    print("📡 Status Code:", res.status_code)

    if res.status_code != 200:
        print("❌ API Error:", res.text)
        return

    data = res.json()
    results = data.get("results", [])

    if not results:
        print("❌ No results found.")
        print("📦 Raw API Response:", data)
        return

    print(f"✅ Found {len(results)} places. Showing top 5:\n")

    for i, place in enumerate(results[:5], 1):
        name = place.get("name", "N/A")
        address = place.get("formatted_address", "N/A")
        rating = place.get("rating", "N/A")
        print(f"{i}. {name}")
        print(f"   📍 Address: {address}")
        print(f"   ⭐ Rating: {rating}\n")

# 🔍 TEST THIS:
search_google_places("veg restaurants", "Hyderabad")
