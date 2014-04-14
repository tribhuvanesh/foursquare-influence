import datetime, time
import sys

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
MIN_CHECKINS = 2
# NEW_EPOCH = 1262304000 # 1-Jan-2010
NEW_EPOCH = 1293840000 # 1-Jan-2011

def main():
    # fin = open('zurich/checkins-zurich-renum.txt', 'r')
    # fout = open('zurich/cascades-zurich-renum.txt', 'w')
    # fusers = open('zurich/users-zurich-renum.txt', 'r')
    # fin = open('sf/checkins-sf-renum.txt', 'r')
    # fout = open('sf/cascades-sf-renum.txt', 'w')
    # fusers = open('sf/users-sf-renum.txt', 'r')
    # fin = open('london/checkins-london-renum.txt', 'r')
    # fout = open('london/cascades-london-renum.txt', 'w')
    # fusers = open('london/users-london-renum.txt', 'r')
    fin = open('rome/checkins-rome-renum.txt', 'r')
    fout = open('rome/cascades-rome-renum.txt', 'w')
    fusers = open('rome/users-rome-renum.txt', 'r')
    # fin = open('checkins-sf.txt', 'r')
    # fout = open('cascades-sf.txt', 'w')
    # fusers = open('users-sf.txt', 'r')
    # fusers = open('users_300.txt', 'r')

    # Read all valid users and create a set
    # Also write all the users as-is to output cascades file
    valid_uids = set()
    for line in fusers:
        uid, uname = line.split(',')
        valid_uids.add( int(uid) )
        fout.write(line)

    # Separator between users and cascades
    fout.write('\n')

    # Skip the header
    fin.readline()

    cur_location = 0
    cascade = set()
    cascade_id = 0

    for line in fin:
        _location, _user, _ts = line.split(',')
        location = int(_location)
        user = int(_user)
        ts = datetime.datetime.strptime(_ts.strip(), TIME_FORMAT)
        ts_int = int(ts.strftime('%s'))

        if location == cur_location:
            cascade.add( (location, user, ts_int) )
        else:
            dct = {}
            for _location, _user, _ts in cascade:
                if _user in valid_uids:
                    dct[_user] = dct.get(min(_ts, dct.get(_user, sys.maxint)), _ts)
            if len(dct.keys()) >= MIN_CHECKINS:
                print 'Dumping %d infections for cascade %d' % (len(cascade), cascade_id)
                # Dump everything in cascade into file as a single cascade
                fout.write("%d;" % cascade_id)
                # Take lowest value of check-ins for each user
                to_write = ''
                # for _location, _user, _ts in cascade:
                #     to_write += "%d,%d," % (_user, _ts)
                for _user, _ts in dct.items():
                    # to_write += "%d,%.2f," % (_user, float(round(_ts, -3)))
                    day = (_ts - NEW_EPOCH)/(60.0 * 60.0 * 24.0)
                    to_write += "%d,%d," % (_user, int(round(day)))
                fout.write('%s\n' % to_write[:-1])
                cascade_id += 1
            else:
                print 'Skipping cascade %d with checkins %d.' % (cascade_id, len(cascade))

            # Begin a new cascade with this location
            cascade = set( [ (location, user, ts_int), ] )
            cur_location = location

    # # Dump residuals
    # print 'Dumping %d infections for cascade %d' % (len(cascade), cur_location)
    # # Dump everything in cascade into file as a single cascade
    # fout.write("%d;" % cascade_id)
    # for _location, _user, _ts in cascade:
    #     fout.write("%d,%d," % (_user, _ts))
    # fout.write('\n')

    fin.close()
    fout.close()


if __name__ == '__main__':
    main()
