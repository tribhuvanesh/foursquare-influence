from geopy.distance import *
import pyprind


Zurich = (47.4787213, 9.4918484)
SF = (37.733436, -122.4343381)
London = (51.5005135, -0.1274967)
Paris = (48.821236, 2.271731)
Rome = (41.8637027, 12.4697898)
RADIUS = 100 # in kilometers

# Enter location here from above
NEAR_LOCATION = Paris

# Other constants
WCL = 2290997

def main():
    fin = open('FoursquareCheckins20110101-20111231.csv')
    fout = open('FoursquareCheckins20110101-20111231_near_paris.csv', 'w')

    # Fancy progress bar
    my_prperc = pyprind.ProgPercent(WCL)

    # Skip the header
    fin.readline()

    for line in fin:
        vals = line[:-2].split(',')
        lat, long = map(float, [vals[1], vals[2]])
        this_location = (lat, long)
        if vincenty(NEAR_LOCATION, this_location) <= RADIUS:
            fout.write(line[:-2])
            fout.write('\n')
        my_prperc.update()

    fin.close()
    fout.close()


if __name__ == '__main__':
    main()
