"""
Created By David Camelo on 10/31/2024

This are the steps to extract Medalists data from first Modern Olympic Games
to Olympic Winter Games Beijing 2022
"""

import pandas as pd
from ExtractingMedalist import OlympicsScraper

# Cargar las URLs del CSV
urls = pd.read_csv("past_olympics.csv")
cities = urls["City"].iloc[49:].tolist()
print(cities)

# Crear la lista completa de URLs
first_part = "https://olympics.com/en/olympic-games/"
last_part = "/athletes"
path = []

for city in cities:
    full_url = f"{first_part}{city}{last_part}"
    path.append(full_url)

# Crear una instancia del scraper
scraper = OlympicsScraper()

# Intenta cargar datos previos del archivo temporal
try:
    existing_data = pd.read_csv("Olympic_medalists_temp.csv")
    header_written = (
        True  # Si ya existe el archivo, se asume que el encabezado ya fue escrito
    )
except FileNotFoundError:
    existing_data = pd.DataFrame()
    header_written = False

for site in path:
    try:
        print(f"Procesando: {site}")
        # Extrae datos de la URL actual
        medalists = scraper.scrape_athletes(site)
        # Agrega los datos actuales al CSV temporal después de cada iteración
        medalists.to_csv(
            "Olympic_medalists_temp.csv",
            mode="a",
            header=not header_written,
            index=False,
        )
        print(f"Datos de {site} guardados temporalmente.")

        # Concatena los datos con los existentes en caso de ya tener previos
        existing_data = pd.concat([existing_data, medalists], ignore_index=True)

    except Exception as e:
        print(f"Error al procesar {site}: {e}")

# Cerrar el navegador


# Renombrar el archivo temporal final a nombre definitivo
existing_data.to_csv("Olympic medalists.csv", index=False)
print("Datos guardados en Olympic medalists.csv")
scraper.close()
