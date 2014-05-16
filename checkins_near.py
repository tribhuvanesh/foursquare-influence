from geopy.distance import *
import pyprind
import sys


loc_dict = {
    'zurich' : (47.4787213, 9.4918484),
    'sf'     : (37.733436, -122.4343381),
    'la'     : (33.7444613, -118.3870173),
    'ny'     : (40.7398242, -73.9354153),
    'boston' : (42.2973205, -71.0744952),
    'chicago': (41.7697533, -87.9358931),
    'seattle': (47.348433, -122.3234561),
    'london' : (51.5005135, -0.1274967),
    'paris'  : (48.821236, 2.271731),
    'rome'   : (41.8637027, 12.4697898),
}
RADIUS = 100 # in kilometers

# Other constants
WCL = 2290997
# WCL = 396635

def main():
    if len(sys.argv) < 3:
        sys.exit('Format: checkins_near input_checkins_file socialgraph [location1] [location2] ...')

    if len(sys.argv) > 3:
        locations = sys.argv[3:]
    else:
        locations = loc_dict.keys()

    socialgraph = sys.argv[2]

    for location in locations:
        print '---- %s ----' % location.upper()
        fin = open(sys.argv[1])
        out_file_name = sys.argv[1].split('.')[0] + '_near_' + location + '.csv'
        sg_out_fname = 'frienship-%s.csv' % location
        fout = open(out_file_name, 'w')

        lines_written = 0

        # Fancy progress bar
        my_prperc = pyprind.ProgPercent(WCL)

        # Skip the header
        fin.readline()

        user_ids = set()

        for line in fin:
            vals = line[:-2].split(',')
            uid = int(line[:-2].split(',')[0])
            lat, long = map(float, [vals[1], vals[2]])
            this_location = (lat, long)
            if vincenty(loc_dict[location], this_location) <= RADIUS:
                user_ids.add(uid)
                fout.write(line[:-2])
                fout.write('\n')
                lines_written += 1
            my_prperc.update()

        print
        print '#Checkins written: ', lines_written

        lines_written = 0
        with open(socialgraph, 'r') as fsg, open(sg_out_fname, 'w') as fout_sg:
            for line in fsg:
                u1, u2 = map(int, line.split(','))
                if u1 in user_ids and u2 in user_ids:
                    fout_sg.write('%d,%d\n' % (u1, u2))
                    lines_written += 1
        print 'Edges written: ', lines_written

        fout.close()
        fin.close()


if __name__ == '__main__':
    main()
