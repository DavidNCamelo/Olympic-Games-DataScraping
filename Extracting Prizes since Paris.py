"""
Created By David Camelo on 11/06/2024
Helped by Chatgpt


This is the source to extract data from Olympic Games since Paris 2024 and
Concatenate the resutls into the full file
"""

from bs4 import BeautifulSoup
import requests
from ExtractDataSinceParis import OlympicScrapperNew
import pandas as pd

# Cargar las URLs del CSV
urls = pd.read_csv("past_olympics.csv")
cities = urls["City"].iloc[0:1].tolist()
print(cities)

# Headers para simular un navegador real
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# Crear la lista completa de URLs
first_part = "https://olympics.com/en/"
last_part = "/medals"
path = []

# Generar la URL completa
for city in cities:
    full_url = f"{first_part}{city}{last_part}"
    path.append(full_url)

# Intenta cargar datos previos
try:
    existing_data = pd.read_csv("Olympic Prizes.csv")
    header_written = (
        True  # Si ya existe el archivo, se asume que el encabezado ya fue escrito
    )
except FileNotFoundError:
    existing_data = pd.DataFrame()
    header_written = False

# Llamar función de scraper
scrap = OlympicScrapperNew()

for site in path:
    # Obtener la respuesta de la página
    response = requests.get(site, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    event = scrap.extract_event(soup)
    prized = scrap.extract_prizes_list(soup)

    # Concatena los datos con los existentes en caso de ya tener previos
    existing_data = pd.concat([existing_data, prized], ignore_index=True)

print(prized)

# Guardar el archivo finalizado
existing_data.to_csv("Olympic Prizes.csv", index=False)
print("Datos guardados en Olympic Prizes.csv")
print(len(existing_data))
