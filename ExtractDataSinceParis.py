"""
Created By David Camelo on 11/06/2024
Helped by Chatgpt


This is the source to extract data from Olympic Games since Paris 2024
"""

# Required Libraries
import pandas as pd
import json
import re


class OlympicScrapperNew:
    def __init__(self):
        self.prizes = pd.DataFrame()  # Initialize DataFrame for these medals
        self.medalists = pd.DataFrame()  # Initialize DataFrame for these medalists

    def extract_prizes_list(self, soup):
        # Search for the json data structure
        scripts = soup.find_all("script")

        # Review all Scripts and retrieve just the Json format
        for sc in scripts:
            if "organisation" in sc.text:  # Search key values from the Json
                json_text_match = re.search(
                    r"\{.*\}", sc.text
                )  # Try to retrieve the fill Json
                if json_text_match:
                    json_text = json_text_match.group()
                    data_json = json.loads(json_text)
                    # print(data_json)
                    break

        # Once known the levels, retrive the required data labels
        if (
            "props" in data_json
            and "pageProps" in data_json["props"]
            and "initialMedals" in data_json["props"]["pageProps"]
            and "medalStandings" in data_json["props"]["pageProps"]["initialMedals"]
        ):
            # Access into medalTable level
            medaltable = data_json["props"]["pageProps"]["initialMedals"][
                "medalStandings"
            ].get("medalsTable", [])

            # Create empty list
            data = []

            # Iterate through each row into medalTable
            for prz in medaltable:
                # Skip the first line, this isn't necessary to retrieve
                if (
                    isinstance(prz, dict)
                    and "organisation" in prz
                    and prz["organisation"]
                ):
                    country = prz.get("organisation")  # Country ISO code
                    medals = prz.get("medalsNumber", [])

                    # Search the subdictionary with Total
                    total_medals = next(
                        (item for item in medals if item["type"] == "Total"), None
                    )

                    if total_medals:
                        # Extract medals lists
                        gold = total_medals.get("gold", 0)
                        silver = total_medals.get("silver", 0)
                        bronze = total_medals.get("bronze", 0)

                        # Append data into each list
                        data.append(
                            {
                                "Event Name": self.event_name,
                                "Country Code": country,
                                "Gold": gold,
                                "Silver": silver,
                                "Bronze": bronze,
                            }
                        )

        # Save data into a DataFrame
        self.prizes = pd.DataFrame(data)

        return self.prizes

    # Extract the Olympic name event from the new web page format
    def extract_event(self, soup):
        # Retrive Event Name
        self.event_name = next(
            (
                img.get("alt")
                for img in soup.find_all("img", alt=True)
                if "Olympic" in img.get("alt")
            ),
            None,
        )

        return self.event_name

    def extract_medalists(self, soup):
        scripts = soup.find_all("script")

        # Review all Scripts and retrieve just the Json format
        for sc in scripts:
            if "organisation" in sc.text:  # Search key values from the Json
                json_text_match = re.search(
                    r"\{.*\}", sc.text
                )  # Try to retrieve the fill Json
                if json_text_match:
                    json_text = json_text_match.group()
                    medal_json = json.loads(json_text)
                    break

        # Once known the levels, retrive the required data labels
        if (
            "props" in medal_json
            and "pageProps" in medal_json["props"]
            and "initialMedallist" in medal_json["props"]["pageProps"]
        ):
            medalist_table = medal_json["props"]["pageProps"]["initialMedallist"].get(
                "athletes", []
            )
            # print(medalist_table)

            # Create empty list
            data2 = []

            # Iterate and extract all required values
            for mdl in medalist_table:
                country = mdl.get("organisation")
                athlete = mdl.get("fullName")
                gold_medals = mdl.get("medalsGold")
                silver_medals = mdl.get("medalsSilver")
                bronze_medals = mdl.get("medalsBronze")
                medals = mdl.get("medals", [])

                # Retrieve only the disciplineName from the first medal entry, if available
                discipline = medals[0].get("disciplineName")

                # Create the final dataframe
                data2.append(
                    {
                        "Event": self.medalist_event_name,
                        "Country": country,
                        "Athlete": athlete,
                        "Sport": discipline,
                        "Gold": gold_medals,
                        "Silver": silver_medals,
                        "Bronze": bronze_medals,
                    }
                )

        # Save data into a new Dataframe
        self.medalists = pd.DataFrame(data2)

        return self.medalists

    def extract_medalist_event(self, soup):
        # Retrieve just the important part according with the existint schema
        self.medalist_event_name = next(
            (
                img.get("alt")
                for img in soup.find_all("img", alt=True)
                if "Olympic" in img.get("alt")
            ),
            None,
        )
        self.medalist_event_name = self.medalist_event_name.replace(
            "Olympic Games ", ""
        ).strip()  # Extract just city and year of the event

        return self.medalist_event_name
