from geopy.distance import *


ZURICH = (37.7833, -122.4167)
#ZURICH = (47.3667, 8.5500)
RADIUS = 100  # in kilometers
filename = "SHTiesData/FoursquareCheckins.csv"


def main():
    fin = open(filename)
    fout = open('only_zurich.out', 'w')

    # Skip the header
    fin.readline()

    for line in fin:
        vals = line[:-2].split(',')
        lat, long = map(float, [vals[1], vals[2]])
        this_location = (lat, long)
        if vincenty(ZURICH, this_location) <= RADIUS:
            fout.write(line[:-2])
            fout.write('\n')

    fin.close()
    fout.close()


if __name__ == '__main__':
    main()
