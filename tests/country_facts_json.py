import json

# A test to find country facts through the factbook.json file.
with open("../data/factbook.json") as data:
    factbook = json.load(data)

print(list(factbook))
print(list(factbook['countries']))
print(list(factbook['countries']['united_kingdom']))
print(list(factbook['countries']['united_kingdom']['data']['people']['population']))
print(factbook['countries']['united_kingdom']['data']['people']['population']['total'])     # yikes, that's a lot


