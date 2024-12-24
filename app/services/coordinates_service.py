import requests
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

def get_coordinates(country, city):
    url = f"https://api.opencagedata.com/geocode/v1/json?q={city}%2C+{country}&key=3aae6f1c03d9446ba8ef93bbf81dd851"
    response = requests.get(url)
    return response.json()