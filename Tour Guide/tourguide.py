import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import ollama
from geopy.geocoders import Nominatim

# Initialize conversation history
convo = []

def stream_response(prompt):
    convo.append({'role': 'user', 'content': prompt})
    response = ''
    stream = ollama.chat(model='llama3.1:8b', messages=convo, stream=True)

    for chunk in stream:
        response += chunk['message']['content']
        print(chunk['message']['content'], end='', flush=True)
    convo.append({'role': 'assistant', 'content': response})
    return response

# Streamlit UI
st.title("AI-Powered Tour Guide Application")

# User Preferences
st.header("Personalized Recommendations")
interests = st.text_input("Enter your interests (comma separated):", "history, architecture")
hobbies = st.text_input("Enter your hobbies (comma separated):", "photography, reading")
food_habits = st.selectbox("Select your food habit:", ["Vegetarian", "Non-Vegetarian"])

# GPS-based Navigation
st.header("GPS-based Navigation")
location = st.text_input("Enter your location (address or landmark):")

# Geolocator for fetching coordinates
geolocator = Nominatim(user_agent="tour_guide_app")

if st.button("Get Nearby Sites"):
    if location:
        # Use geopy to fetch coordinates based on user location input
        loc = geolocator.geocode(location)
        
        if loc:
            data = pd.DataFrame({
                'latitude': [loc.latitude],
                'longitude': [loc.longitude]
            })
            st.map(data, zoom=12)
            st.write(f"Latitude: {loc.latitude}, Longitude: {loc.longitude}")
            st.write("Fetching nearby historical sites...")
            # Simulated nearby sites (this should ideally be fetched from an external API)
            st.write("Nearby sites: Example Site 1, Example Site 2")
            
        else:
            st.error("Location not found. Please enter a valid location.")
    else:
        st.error("Please enter a location.")

# Content Generation using Llama 3
st.header("Tour Guide Application Tasks")

def run_tour_guide_tasks():
    # Prepare the prompt for llama3
    prompt = f"Based on the following preferences: Interests: {interests}, Hobbies: {hobbies}, Food Habits: {food_habits}, generate a personalized tour guide recommendation. at {location}"
    output = stream_response(prompt=prompt)
    return output

if st.button("Run Tour Guide Tasks"):
    output = run_tour_guide_tasks()
    st.write(output)

# Download content for offline mode
st.header("Offline Mode")
site_info = st.text_area("Site information to download:", "This is detailed information about the site.")
if st.button("Download Site Info"):
    if site_info:
        with open("site_info.txt", "w") as file:
            file.write(site_info)
        st.success("Site information downloaded successfully!")
    else:
        st.error("Please enter site information to download.")