"""
Created By David Camelo on 02/27/2026

Extract Medalists data using official Olympics API
(Milano-Cortina 2026 compatible)
"""

import pandas as pd
from ExtractingMilano import OlympicScrapperNew

# -----------------------------
# Cargar eventos desde CSV
# -----------------------------
urls = pd.read_csv("past_olympics.csv")
cities = urls["City"].iloc[0:1].tolist()  # Ajusta slice según necesidad
print(cities)

# -----------------------------
# Crear instancia del scraper
# -----------------------------
scraper = OlympicScrapperNew()

# -----------------------------
# Intentar cargar archivo temporal
# -----------------------------
try:
    existing_data = pd.read_csv("Olympic_medalists_temp.csv")
    header_written = True
except FileNotFoundError:
    existing_data = pd.DataFrame()
    header_written = False

# -----------------------------
# Loop por eventos
# -----------------------------
for city in cities:

    try:
        print(f"Procesando evento: {city}")

        scraper.base_api = "https://www.olympics.com/wmr-owg2026/competition/api/ENG"
        scraper.event_name = scraper.format_event_name(city)

        medalists = scraper.extract_medalists()

        if medalists is None or medalists.empty:
            print(f"No se encontraron medallistas para {city}")
            continue

        # Guardado incremental (seguro ante fallos)
        medalists.to_csv(
            "Olympic_medalists_temp.csv",
            mode="a",
            header=not header_written,
            index=False,
        )

        header_written = True

        # Concatenación en memoria
        existing_data = pd.concat([existing_data, medalists], ignore_index=True)

        print(f"Datos de {city} guardados temporalmente.")

    except Exception as e:
        print(f"Error procesando {city}: {e}")

# -----------------------------
# Guardado final
# -----------------------------
try:
    final_data = pd.read_csv("Olympic medalists.csv")
except FileNotFoundError:
    final_data = pd.DataFrame()

    # Appending
combined = pd.concat([final_data, existing_data], ignore_index=True)

# Deleting duplicates
combined.drop_duplicates(subset=["Event", "Athlete", "Country"], inplace=True)

combined.to_csv("Olympic medalists.csv", index=False)

print("Datos guardados en Olympic medalists.csv")
print(f"Total registros: {len(existing_data)}")
