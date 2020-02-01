import pandas as pd
import reverse_geocode as rg

# what we want a function to do:
# 1 - takes in a latitude + longitude
# 2 - gets the nearest country
# 3 - gets the 3 basic properties: population, gdp, area (or none at all)
# 4 - gets the 5 running trends

pd.options.display.max_columns = 10
valid_locations = {'Austria', 'Belgium', 'Czech Republic', 'Denmark', 'Finland', 'France',
                   'Germany', 'Greece', 'Hungary', 'Ireland', 'Italy', 'Netherlands', 'Norway',
                   'Poland', 'Portugal', 'Romania', 'Russia', 'Sweden', 'Switzerland', 'Turkey',
                   'Ukraine', 'United Kingdom', 'India', 'Indonesia', 'Israel', 'Japan',
                   'Malaysia', 'Philippines', 'Russia', 'Saudi Arabia', 'Singapore',
                   'South Korea', 'Taiwan', 'Thailand', 'Turkey', 'Vietnam', 'Egypt', 'Kenya',
                   'Nigeria', 'South Africa', 'Canada', 'Mexico', 'United States', 'Argentina',
                   'Brazil', 'Chile', 'Colombia', 'Australia'}


def get_info(latitude, longitude):
    coordinates = (latitude, longitude)
    country = rg.search([coordinates])[0]['country']
    code = rg.search([coordinates])[0]['country_code']  # for finding the flag

    # hard code
    # Russian federation -> Russia
    # Korea, Republic of -> South Korea
    # Korea, Democratic People's Republic of -> North Korea
    name_map = {
        "Russian Federation": "Russia",
        "Korea, Republic of": "South Korea",
        "Korea, Democratic People's Republic of": "North Korea"
    }

    if country in name_map:
        country = name_map[country]

    # --- Get country facts ---
    arr_facts = get_country_facts(country)

    # --- Get trends ---
    arr_trends = get_country_trends(country)

    # return [country] + arr_facts + arr_trends     # if returning as a single array
    return country, arr_facts, arr_trends


def get_country_trends(country):
    df = pd.read_csv("../data/TrendsByCountry.csv")
    trends = df[df['country'] == country][['trend1', 'trend2', 'trend3', 'trend4', 'trend5']]

    if len(trends) < 1:
        return None

    arr_trends = [trends.values[0][i] for i in range(5)]
    return arr_trends


def get_country_facts(country):
    df = pd.read_csv("../data/country_profile_variables.csv")

    # rename population, gdp and area
    df['population'] = df['Population in thousands (2017)'] * 1000
    df = df.rename(columns={'GDP: Gross domestic product (million current US$)': 'gdp', 'Surface area (km2)': 'area'})
    df.loc[df['gdp'] == -99, 'gdp'] = "N/A"  # rename negative GDP values

    facts = df[df['country'] == country]

    if len(facts) < 1:
        return None

    population = facts['population'].values[0]  # actual value
    gdp = str(facts['gdp'].values[0]) + " million ($US)"  # $US millions
    area = str(facts['area'].values[0]) + " km^2"  # km^2
    arr_facts = [population, gdp, area]

    return arr_facts


# testing: Should give India
# print(get_info(28.5, 77.2))
# testing: Should return None
# print(get_info(0, 0))
print(rg.search([(57, -141)]))
