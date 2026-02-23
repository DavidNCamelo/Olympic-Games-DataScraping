"""
Created by David Camelo helped by ChatGPT 09/23/2024

This are the steps to extract Countries and Prizes from first Modern Olympic Games
to Olympic Winter Games Beijing 2022
"""

# Import Required Libraries
import pandas as pd


class medals_list:

    def __init__(self):
        self.country_code = []  # Initialize ISO Code list
        self.cts_name = []  # Initialize Country Name list
        self.prizes = pd.DataFrame()  # Initialize DataFrame for medals
        self.country_df = pd.DataFrame(
            columns=["Country Code", "Country Name"]
        )  # Initialize DataFrame for country codes and names

    # Extract a list of countries that have won medals in each Olympic session
    def extract_country_list(self, soup):

        # Reset values for the next sessions and be added correctly over the medals dataframe
        self.country_code = []
        self.cts_name = []

        # Serch for the items where are located the countries information
        country = soup.find_all("div", {"data-row-id": True})

        # Serch for parser and extact information
        for mds in country:
            # Search for the ISO Codes
            ISO_code = mds.find("div", {"data-cy": "tri-letter-code"})
            if ISO_code:
                ISO_code = ISO_code.text
                self.country_code.append(ISO_code)

            # print(ISO_code)

            # Search for the Countries Names
            country_name = mds.find("span", {"data-cy": "country-name"})
            if country_name:
                country_name_text = country_name.text
                self.cts_name.append(country_name_text)

                # Create a country Dataframe
                self.country_df = pd.concat(
                    [
                        self.country_df,
                        pd.DataFrame(
                            {
                                "Country Code": [ISO_code],
                                "Country Name": [country_name_text],
                            }
                        ),
                    ],
                    ignore_index=True,
                )
            # print(country_name_text)

        # Keep unique values into the DataFrame
        self.country_df = self.country_df.drop_duplicates()

        return self.country_code, self.cts_name

    # Extract total won medals by the teams
    def extract_medals(self, soup):

        medals_div = soup.find_all("div", {"data-cy": "medal-module"})

        medal_data = []

        # Filter and sort medal quantities
        current_country_medals = {}
        for row in medals_div:
            medal_type = row["data-medal-id"]
            medal_count = row.find("span", {"data-cy": "ocs-text-module"}).text
            medal_count = 0 if medal_count == "-" else medal_count

            # Retrieve just those lines where containd the Gold, Silver and Bronze
            if "gold" in medal_type:
                current_country_medals["gold"] = medal_count
            elif "silver" in medal_type:
                current_country_medals["silver"] = medal_count
            elif "bronze" in medal_type:
                current_country_medals["bronze"] = medal_count

            # Add data just when required
            if len(current_country_medals) == 3:
                if (
                    self.country_code and self.cts_name
                ):  # Ensure country lists are populated
                    country_info = {
                        "Event Name": self.name,
                        "Country Code": self.country_code.pop(
                            0
                        ),  # Get the corresponding country code
                        "Gold": current_country_medals["gold"],
                        "Silver": current_country_medals["silver"],
                        "Bronze": current_country_medals["bronze"],
                    }
                    medal_data.append(country_info)
                current_country_medals = {}

        medal_df = pd.DataFrame(medal_data)

        self.prizes = pd.concat([self.prizes, medal_df], ignore_index=True)

        return self.prizes

    # Extract the name from the h2 element
    def extract_name(self, soup):
        name_element = soup.find("h2")
        self.name = name_element.text

        return self.name


# End of the function
