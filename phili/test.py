# Python3 program for reverse geocoding.

# importing necessary libraries
import reverse_geocode as rg
import pprint


def reverseGeocode(coordinates):
    result = rg.search(coordinates)

    # result is a list containing ordered dictionary.
    pprint.pprint(result)


# Driver function
if __name__ == "__main__":
    # Coorinates tuple.Can contain more than one pair.
    coordinates = (28.613939, 77.209023)

    reverseGeocode(coordinates)