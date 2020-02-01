import pandas as pd

# Finding country facts through using a CSV file
pd.options.display.max_rows = 10
pd.options.display.max_columns = 10

df = pd.read_csv("../data/country_profile_variables.csv")
df = df.set_index(['country'])


# population
df['population'] = df['Population in thousands (2017)'] * 1000

# gdp
df = df.rename(columns={'GDP: Gross domestic product (million current US$)': 'gdp', 'Surface area (km2)': 'area'})

df.loc[df['gdp'] == -99, 'gdp'] = "N/A"

print(df[['population', 'gdp', 'area']])

# retrieve countries only in trends by country
country = pd.read_csv("../data/TrendsByCountry.csv")
print(country)
