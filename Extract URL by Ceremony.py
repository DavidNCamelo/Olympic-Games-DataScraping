"""
Created by David Camelo 09/23/2024

Extracting Olympics URLS
"""

# Import Required Libraries
import requests
from bs4 import BeautifulSoup as bs
import json
import pandas as pd

# Official Olympcs web site
olympic_url = "https://olympics.com/en/olympic-games"

# Requests Headers
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

# GET on page
response = requests.get(olympic_url, headers=header)

# Parser through BeautifulSoup
soup = bs(response.content, "html.parser")

# Search into Json schema
script_tag = soup.find("script", type="application/ld+json")

# If TRUE continue extracting
if script_tag:
    json_content = script_tag.string

    # Load Json into a dictitionary
    data = json.loads(json_content)

    # Verificamos si existe el ItemList y lo procesamos
    if "@type" in data and data["@type"] == "ItemList":
        items = data.get("itemListElement", [])

        # #Create list and extract url section
        urls = []
        sections = []

        for item in items:
            url = item["url"]
            # Extract section after the last "/"
            section = url.split("/")[-1]

            # Save lists
            urls.append(url)
            sections.append(section)

        # Create DataFrame to be saved into a file
        df = pd.DataFrame({"URL": urls, "City": sections})

        # Show table
        # print(df)
    else:
        print("Didn't find any ItemLinst in JSON.")
else:
    print("Didn't find <script> with JSON-LD.")

# past olympics
past_olympic = df[5:]

past_olympic.to_csv("past_olympics.csv", index=False)
