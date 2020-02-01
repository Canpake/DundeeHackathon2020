import reverse_geocode
import numpy as np

for x in range(100):
    lat = (np.random.random()-0.5)*180
    long = (np.random.random()-0.5)*360
    coordinates = (lat, long)
    print(coordinates)
    print(reverse_geocode.search([coordinates]))
