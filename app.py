import os
import requests
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Load API keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# Function to call Google Places Text Search
def search_google_places(query, location):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": f"{query} in {location}",
        "key": GOOGLE_API_KEY
    }
    res = requests.get(url, params=params)
    if res.status_code == 200:
        return res.json().get("results", [])
    else:
        return []

# Format places into markdown
def format_place_info(places):
    lines = []
    for i, place in enumerate(places[:5], 1):
        name = place.get("name", "Unknown")
        address = place.get("formatted_address", "N/A")
        rating = place.get("rating", "N/A")
        lines.append(f"{i}. **{name}**\n📍 {address}\n⭐ Rating: {rating}\n")
    return "\n".join(lines)

# Streamlit UI
st.set_page_config(page_title="Restaurant/Hotel Recommender")
st.title("🍽️ Restaurant & Hotel Recommender")
st.markdown("Ask me about great places to eat or stay in any city!")

with st.form("chat_form"):
    user_input = st.text_input("Where and what are you looking for?", placeholder="e.g., best veg restaurants in Hyderabad")
    submitted = st.form_submit_button("Ask")

if submitted and user_input:
    with st.spinner("🔎 Searching..."):
        # Try to extract query and location from input
        if " in " in user_input:
            parts = user_input.split(" in ", 1)
            query = parts[0]
            location = parts[1]
        else:
            query = user_input
            location = "India"  # fallback

        places = search_google_places(query, location)

        if not places:
            st.error("No places found. Try a different area or spelling.")
        else:
            place_md = format_place_info(places)
            st.markdown("### 📍 Top Places Found:")
            st.markdown(place_md)

            # Ask Gemini to recommend
            names = [p['name'] for p in places[:5]]
            prompt = f"These are some places found for {query} in {location}: {', '.join(names)}. Which of these would you most recommend and why?"
            response = model.generate_content(prompt)
            st.markdown("### 💬 Gemini Suggests:")
            st.write(response.text)
