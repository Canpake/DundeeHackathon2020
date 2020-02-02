import wikipedia


def get_data(country):
    sentences = str(wikipedia.summary(country, sentences = 5))
    return sentences


print(get_data("United States"))
get_data("Myanmar")
get_data("kiribas")