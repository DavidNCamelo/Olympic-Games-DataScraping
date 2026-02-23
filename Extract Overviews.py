"""
Created by David Camelo helped by ChatGPT 10/26/2024

Overview from Olympics URL's saved documents
"""

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from Overviews import over_view_info

# Required Header
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

# Initialize dataframe
countrylist = pd.DataFrame(columns=["Olympic Session", "Country Order"])

# Load the csv's rows
urls = pd.read_csv("past_olympics.csv")

cities = urls["City"].iloc[0:1].tolist()

# Create the full url list
first_part = "https://olympics.com/en/olympic-games/"

path2 = []

# Read the cities list and concatenate the full link to extract all required information
for ct in cities:
    full_link = f"{first_part}{ct}"
    path2.append(full_link)

    # Initialize the called class
    scap = over_view_info()

    # Iterate and extract
    for lk in path2:
        responses2 = requests.get(lk, headers=header)
        soup2 = bs(responses2.content, "html.parser")

        events = scap.extract_name(soup2)
        logo = scap.extract_image(soup2)
        overs = scap.extract_overview(soup2)

# Save into simple dataframe
full_overview = scap.overview_dataf

# Cargar el archivo existente
try:
    existing_data = pd.read_csv("Olympic Overview.csv")
except FileNotFoundError:
    existing_data = pd.DataFrame()

# Combinar con los nuevos datos
full_data = pd.concat([existing_data, full_overview], ignore_index=True)

# Guardar todo junto
full_data.to_csv("Olympic Overview.csv", index=False)
