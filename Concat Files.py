"""
Created By David Camelo on 10/24/2024
"""

# Import Required Libraries
import pandas as pd

# List each required file to be concatenated

# First the Olympic received prizes

prizes1 = pd.read_csv("Olympic Prizes First Part.csv")
prizes2 = pd.read_csv("Olympic Prizes second Part.csv")
prizes3 = pd.read_csv("Olympic Prizes third Part.csv")
prizes4 = pd.read_csv("Olympic Prizes fourth Part.csv")
prizes5 = pd.read_csv("Olympic Prizes fifth Part.csv")

full_prizes = pd.concat(
    [prizes1, prizes2, prizes3, prizes4, prizes5], ignore_index=True
)

# Save the final file
full_prizes.to_csv("Olympic Prizes.csv", index=False)

# Verify if where saved
print("Full Prizes succesfull saved!!!")


# Now the countries list, saving distinct values

countries1 = pd.read_csv("Olympic Countries first part.csv")
countries2 = pd.read_csv("Olympic Countries second part.csv")
countries3 = pd.read_csv("Olympic Countries third part.csv")
countries4 = pd.read_csv("Olympic Countries fourth part.csv")
countries5 = pd.read_csv("Olympic Countries fifth part.csv")

# Concatenate all countries files
full_countries = pd.concat(
    [countries1, countries2, countries3, countries4, countries5], ignore_index=True
)

# Drop duplicated rows
full_countries = full_countries.drop_duplicates()

# Save the final countries files
full_countries.to_csv("Olympic Countrires.csv", index=False)

# Verify if where saved
print("Full Countries succesfull saved!!!")
