"""
Created By David Camelo on 11/13/2024
Helped by Chatgpt


This is the source to extract Medalists data from Olympic Games since Paris 2024 and
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
last_part = "/medals/medallists"
path = []

# Generar la URL completa
for city in cities:
    full_url = f"{first_part}{city}{last_part}"
    path.append(full_url)


# Intenta cargar datos previos
try:
    existing_data = pd.read_csv("Olympic medalists.csv")
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

    event = scrap.extract_medalist_event(soup)
    medalists = scrap.extract_medalists(soup)

    # Concatenar datos
    existing_data = pd.concat([existing_data, medalists], ignore_index=True)

print(medalists)

# Guardar archivo final
existing_data.to_csv("Olympic medalists.csv", index=False)
print("Datos guardados en Olympic medalists.csv")
print(len(existing_data))
