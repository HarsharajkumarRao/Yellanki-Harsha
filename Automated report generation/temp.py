import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define API endpoint and parameters
API_URL = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 20.5937,  # India latitude
    "longitude": 78.9629,  # India longitude
    "hourly": "temperature_2m",
    "past_days": 7,  # Get data for the last 7 days
    "timezone": "Asia/Kolkata"
}

# Fetch weather data from API
response = requests.get(API_URL, params=params)
data = response.json()

# Extract time and temperature data
time_series = data["hourly"]["time"]
temperature_series = data["hourly"]["temperature_2m"]

# Create a DataFrame
df = pd.DataFrame({"Time": time_series, "Temperature (°C)": temperature_series})
df["Time"] = pd.to_datetime(df["Time"])  # Convert to datetime format

# Plot the data
plt.figure(figsize=(12, 6))
sns.lineplot(x=df["Time"], y=df["Temperature (°C)"], linewidth=2, marker="o")

# Set plot labels and title
plt.xlabel("Date & Time")
plt.ylabel("Temperature (°C)")
plt.title("Temperature Trends Over Last 7 Days (India)")

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Display the plot
plt.show()
