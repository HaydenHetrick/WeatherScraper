from bs4 import BeautifulSoup
import pandas as pd
import requests

# Function to ask the user if they want to view previous data
def ask_user():
    user_input = input("Do you want to view previous days' weather data (yes/no)?, if user selects no all previous data will be deleted ").lower()
    return user_input == 'yes'

# Check if user wants to view previous data
view_previous_data = ask_user()

url = "https://forecast.weather.gov/MapClick.php?lat=41.0248&lon=-80.7586"
r = requests.get(url)

soup = BeautifulSoup(r.content,"html.parser")
week = soup.find(id="seven-day-forecast-body")
items = soup.find_all("div",class_ = "tombstone-container")
period_name = [item.find(class_="period-name").get_text() for item in items]
short_desc = [item.find(class_="short-desc").get_text() for item in items]
temp = [item.find(class_="temp").get_text() for item in items]

# Load existing CSV data if user wants to view previous data
if view_previous_data:
    try:
        existing_data = pd.read_csv("CanfieldWeatherData.csv")
        print(existing_data)
    except FileNotFoundError:
        print("No existing data found.")

# Create a new DataFrame
df = pd.DataFrame({"Day" : period_name,"Weather" : short_desc,"Highs-Lows" : temp})

# Append new data to existing data (if it exists)
if view_previous_data and 'existing_data' in locals():
    df = pd.concat([existing_data, df], ignore_index=True)

# Save to CSV
df.to_csv("CanfieldWeatherData.csv", index=False)