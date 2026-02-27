"""
Created By David Camelo on 11/06/2024
Updated to API-based extraction (Milano-Cortina 2026 compatible)
"""

# Required Libraries
import pandas as pd
import requests


class OlympicScrapperNew:
    def __init__(self):
        self.prizes = pd.DataFrame()
        self.event_name = None
        self.medalists = pd.DataFrame()

        # Base configuration
        self.base_api = "https://www.olympics.com/wmr-owg2026/competition/api/ENG"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept": "application/json, text/plain, */*",
            "Referer": "https://www.olympics.com/en/milano-cortina-2026/medals",
            "Origin": "https://www.olympics.com",
        }

        self.event_name = "Milano-Cortina 2026"

    # -----------------------------
    # MEDAL TABLE
    # -----------------------------

    def extract_prizes_list(self, soup=None):

        url = f"{self.base_api}/medals"
        response = requests.get(url, headers=self.headers)

        print("Status:", response.status_code)

        if response.status_code != 200:
            print(response.text)
            return None

        data_json = response.json()

        medals_table = data_json["medalStandings"]["medalsTable"]

        data = []

        for country in medals_table:

            country_code = country.get("organisation")

            medals_number = country.get("medalsNumber", [])

            # 🔥 Buscar el objeto donde type == "Total"
            total_block = next(
                (m for m in medals_number if m.get("type") == "Total"), None
            )

            if total_block:

                data.append(
                    {
                        "Event Name": self.event_name,
                        "Country Code": country_code,
                        "Gold": total_block.get("gold", 0),
                        "Silver": total_block.get("silver", 0),
                        "Bronze": total_block.get("bronze", 0),
                    }
                )

        self.prizes = pd.DataFrame(data)

        return self.prizes

    # -----------------------------
    # MEDALISTS (ATHLETES)
    # -----------------------------
    def extract_medalists(self, soup=None):

        url = f"{self.base_api}/medallists"
        response = requests.get(url, headers=self.headers)

        print("Status (medallists):", response.status_code)

        if response.status_code != 200:
            print(response.text)
            return None

        data_json = response.json()
        athletes = data_json.get("athletes", [])

        data2 = []

        for athlete in athletes:

            gold = 0
            silver = 0
            bronze = 0
            sport = None

            medals = athlete.get("medals", [])

            for medal in medals:

                medal_type_raw = medal.get("medalType")

                # 🔥 Normalizar tipo de medalla
                if medal_type_raw == "ME_GOLD":
                    gold += 1
                elif medal_type_raw == "ME_SILVER":
                    silver += 1
                elif medal_type_raw == "ME_BRONZE":
                    bronze += 1

                # Tomar disciplina (solo necesitamos una)
                if not sport:
                    sport = medal.get("disciplineName")

            data2.append(
                {
                    "Event": self.event_name,
                    "Country": athlete.get("organisation"),
                    "Athlete": athlete.get("fullName"),
                    "Sport": sport,
                    "Gold": gold,
                    "Silver": silver,
                    "Bronze": bronze,
                }
            )

        self.medalists = pd.DataFrame(data2)

        return self.medalists

    # -----------------------------
    # EVENT NAME (STATIC NOW)
    # -----------------------------
    def extract_event(self, soup=None):
        return self.event_name

    def extract_medalist_event(self, soup=None):
        return self.event_name

    def format_event_name(self, slug):
        parts = slug.replace("-", " ").split()
        return " ".join(word.capitalize() for word in parts)
