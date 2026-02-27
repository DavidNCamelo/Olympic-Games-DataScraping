"""
Created By David Camelo on 11/06/2024
Updated API-based concatenation
"""

import pandas as pd
from ExtractingMilano import OlympicScrapperNew

# Cargar las URLs del CSV
urls = pd.read_csv("past_olympics.csv")

# Ahora necesitamos el identificador interno del evento
cities = urls["City"].iloc[0:1].tolist()
print(cities)

# Intentar cargar datos previos
try:
    existing_data = pd.read_csv("Olympic Prizes.csv")
except FileNotFoundError:
    existing_data = pd.DataFrame()

scrap = OlympicScrapperNew()

for city in cities:

    # Para Milano-Cortina:
    scrap.base_api = "https://www.olympics.com/wmr-owg2026/competition/api/ENG"
    scrap.event_name = f"Olympic Winter Games {scrap.format_event_name(city)}"

    prized = scrap.extract_prizes_list()

    existing_data = pd.concat([existing_data, prized], ignore_index=True)

print(prized)

existing_data.to_csv("Olympic Prizes.csv", index=False)
print("Datos guardados en Olympic Prizes.csv")
print(len(existing_data))
