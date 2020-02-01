import collections

from pytrends.request import TrendReq

trendRequester = TrendReq(hl='en-US', tz=360)

file = open("TrendsByCountry.csv", "w")
print("This Program helps find trends associated with countries.")
print("It will write the associated 5 trends to a CSV file.")
countries = [

    "Albania", "Andorra", "Armenia", "Austria", "Azerbaijan", "Belarus", "Belgium", "Bosnia and Herzegovina",
    "Bulgaria"
    , "Croatia", "Cyprus", "Czech Republic", "Denmark", "Estonia", "Finland", "France", "Georgia", "Germany", "Greece",
    "Hungary"
    , "Iceland", "Ireland", "Italy", "Kazakhstan", "Kosovo", "Latvia", "Liechtenstein", "Lithuania", "Luxembourg",
    "Macedonia", "Malta", "Moldova"
    , "Monaco", "Montenegro", "Netherlands", "Norway", "Poland", "Portugal", "Romania", "Russia", "San Marino",
    "Serbia", "Slovakia", "Slovenia"
    , "Spain", "Sweden", "Switzerland", "Turkey", "Ukraine", "United Kingdom", "Vatican City"


    , "Afghanistan", "Armenia", "Azerbaijan", "Bahrain", "Bangladesh", "Bhutan", "Brunei", "Cambodia", "China",
    "Cyprus", "Georgia", "India"
    , "Indonesia", "Iran", "Iraq", "Israel", "Japan", "Jordan", "Kazakhstan", "Kuwait", "Kyrgyzstan", "Laos", "Lebanon",
    "Malaysia", "Maldives"
    , "Mongolia", "Myanmar", "Nepal", "North Korea", "Oman", "Pakistan", "Philippines", "Qatar", "Russia",
    "Saudi Arabia", "Singapore", "South Korea"
    , "Sri Lanka", "Syria", "Taiwan", "Tajikistan", "Thailand", "Timor-Leste", "Turkey", "Turkmenistan",
    "United Arab Emirates", "Uzbekistan", "Vietnam"
    , "Yemen"

    , "Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cabo Verde", "Cameroon",
    "Central African Republic", "Chad", "Comoros"
    , "Democratic Republic of the Congo", "Republic of the Congo", "Cote d'Ivoire", "Djibouti", "Egypt",
    "Equatorial Guinea", "Eritrea", "Ethiopia", "Gabon", "Gambia", "Ghana", "Guinea",
    "Guinea-Bissau", "Kenya", "Lesotho"
    , "Liberia", "Libya", "Madagascar", "Malawi", "Mali", "Mauritania", "Mauritius", "Morocco", "Mozambique", "Namibia",
    "Niger", "Nigeria", "Rwanda", "Sao Tome and Principe", "Senegal", "Seychelles", "Sierra Leone", "Somalia",
    "South Africa", "South Sudan", "Sudan", "Swaziland", "Tanzania", "Togo", "Tunisia", "Uganda", "Zambia", "Zimbabwe"


    , "Antigua and Barbuda", "Bahamas", "Barbados", "Belize", "Canada", "Costa Rica", "Cuba", "Dominica",
    "Dominican Republic", "El Salvador", "Grenada", "Guatemala", "Haiti", "Honduras", "Jamaica", "Mexico", "Nicaragua",
    "Panama", "Saint Kitts and Nevis ", "Saint Lucia", "Saint Vincent and the Grenadines", "Trinidad and Tobago",
    "United States"

    , "Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Ecuador", "Guyana", "Paraguay"
    , "Peru", "Suriname", "Uruguay", "Venezuela"


    , "Australia", "Fiji", "Kiribati", "Marshall Islands", "Micronesia", "Nauru", "New Zealand", "Palau",
    "Papua New Guinea", "Samoa", "Solomon Islands", "Tonga", "Tuvalu", "Vanuatu"]


file.write("country,trend1,trend2,trend3,trend4,trend5\n")
all_trends = []
for country in countries:
    try:
        country = country.replace(" ", "_").lower()
        trends = str(trendRequester.trending_searches(pn=country)).split('\n')
        trends = trends[1:6]
        i = 0
        file.write(country.replace('_', " ").title() + ",")
        for trend in trends:
            i += 1
            trend_info = (trend[2:].strip())
            if ',' in trend_info:
                trend_info = "\"" +  trend_info + "\""
            if i < 5:
                file.write(trend_info + ",")
            else:
                file.write(trend_info)
            all_trends.append(trend_info)
        file.write("\n")

    except KeyError:
        # print("Invalid search ", country)
        continue

print(collections.Counter(all_trends).most_common())
