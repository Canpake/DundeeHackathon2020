import wikipedia


def get_data(country):
    print(wikipedia.summary(country, sentences = 5))


get_data("United States")
get_data("Myanmar")
get_data("kiribas")