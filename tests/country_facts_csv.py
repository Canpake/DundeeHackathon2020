import pandas as pd

# Finding country facts through using a CSV file
pd.options.display.max_rows = 230
pd.options.display.max_columns = 10

df = pd.read_csv("../data/country_profile_variables.csv")

# retrieve countries in the TrendsByCountry.csv file
country = pd.read_csv("../data/TrendsByCountry.csv")
country = country['country'].values

# population
df['population'] = df['Population in thousands (2017)'] * 1000

# gdp
df = df.rename(columns={'GDP: Gross domestic product (million current US$)': 'gdp', 'Surface area (km2)': 'area'})

df.loc[df['gdp'] == -99, 'gdp'] = "N/A"

print(df[['country', 'population', 'gdp', 'area']])

# get facts only of countries in TrendsByCountry.csv
df = df[df['country'].isin(country)]
print(df[['country', 'population', 'gdp', 'area']])

# which countries are not shown compared to TrendsByCountry.csv?
print(set(country) - set(df['country'].values))     # no taiwan :(
