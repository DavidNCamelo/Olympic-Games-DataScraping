"""
Created By David Camelo on 10/24/2024
helped by chatgpt

This are the functions class to extract Medalists data from first Modern Olympic Games
to Olympic Winter Games Beijing 2022
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import re


class OlympicsScraper:
    def __init__(self):
        # Setting the chrome action with headless
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome()

    def scrape_athletes(self, url):
        # Navigate through the given urls
        self.driver.get(url)

        # Allow cookies settings if there is the button
        try:
            cookies_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            )
            cookies_button.click()
            print("Cookies aceptadas.")
        except:
            print("Botón de cookies no encontrado o ya aceptado.")

        # Clicking on More button until this won't be available
        scroll_attempts = 0
        max_scroll_attempts = 5  # Max scroll attemps to search the more button
        while True:
            try:
                # Buscar y hacer clic en el botón "More"
                more_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, "button[data-cy='more-button']")
                    )
                )
                more_button.click()
                print("Clic en 'More' realizado, cargando más atletas...")
                scroll_attempts = 0
                time.sleep(2)
            except:
                # If the more button isn't find end the attempts
                scroll_attempts += 1
                self.driver.execute_script("window.scrollBy(0, 300);")
                time.sleep(2)
                # Break the loop
                if scroll_attempts >= max_scroll_attempts:
                    print("No hay más atletas para cargar.")
                    break

        ## Obtain the full html
        soup = BeautifulSoup(self.driver.page_source, "html.parser")

        # Extract the name of the event
        event = soup.find("h1").text.replace("Athletes", "").strip()

        # Extract Athletes data
        athlete_data = soup.find_all("div", {"data-row-id": True})

        # Extract Athletes' sport data
        sport_data = soup.find_all(attrs={"data-row-id": True})

        countries, athletes, sports, gold_medals, silver_medals, bronze_medals = (
            [],
            [],
            [],
            [],
            [],
            [],
        )

        for row in athlete_data:
            # Obtain country
            country = row.find("span", {"data-cy": re.compile(r"^[A-Z]{3}$")})
            if country:
                countries.append(country["data-cy"])

            # Obtain athlete name
            athlete_name_element = row.find("h3", {"data-cy": "athlete-name"})
            if athlete_name_element:
                athlete_name = athlete_name_element.text.strip()
                athletes.append(athlete_name)

            # Extracts the prizes per athlete
            gold_medal = row.find("div", {"data-medal-id": re.compile(r"gold-medals")})
            silver_medal = row.find(
                "div", {"data-medal-id": re.compile(r"silver-medals")}
            )
            bronze_medal = row.find(
                "div", {"data-medal-id": re.compile(r"bronze-medals")}
            )

            # Clean and align the results for the final DataFrame
            if gold_medal and silver_medal and bronze_medal:
                gold = gold_medal.find("span", {"data-cy": "ocs-text-module"}).text
                silver = silver_medal.find("span", {"data-cy": "ocs-text-module"}).text
                bronze = bronze_medal.find("span", {"data-cy": "ocs-text-module"}).text
                gold = "0" if gold == "-" else gold
                silver = "0" if silver == "-" else silver
                bronze = "0" if bronze == "-" else bronze

                # Append into the filling lists
                gold_medals.append(gold)
                silver_medals.append(silver)
                bronze_medals.append(bronze)

        # Extract athletes' sport
        for spr in sport_data:
            sport = spr.find("p", {"data-cy": "sport"})
            if sport:
                sports_A = sport.text.strip()
                sports.append(sports_A)

        # Create the final dataframe
        return pd.DataFrame(
            {
                "Event": event,
                "Country": countries,
                "Athlete": athletes,
                "Sport": sports,
                "Gold": gold_medals,
                "Silver": silver_medals,
                "Bronze": bronze_medals,
            }
        )

    def close(self):
        """Close Browser."""
        self.driver.quit()
