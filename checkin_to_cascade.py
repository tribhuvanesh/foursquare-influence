import datetime, time
import sys
import tempfile

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
MIN_CHECKINS = 2
# NEW_EPOCH = 1262304000 # 1-Jan-2010
# NEW_EPOCH = 1293840000 # 1-Jan-2011
NEW_EPOCH = 1322697600 # 1-Dec-2011
TIME_LIMIT = 350
TIME_INT = 100
INSERT_AUX_NODES = False

def main():
    # fin = open('data/paris-aux/Paris_checkins-renum.txt', 'r')
    # fout = open('data/paris-aux/cascades-paris-renum.txt', 'w')
    # fground = open('data/paris-aux/cascades-paris-ground-truth.txt', 'w')
    # fusers = open('data/paris-aux/friendships-users-renum.txt', 'r')

    fin = open('data/umn/boston/all_checkins_near_boston-renum.txt', 'r')
    fout = open('data/umn/boston/cascades.txt', 'w')
    fground = open('data/umn/boston/cascades-ground-truth.txt', 'w')
    fusers = open('data/umn/boston/frienship-boston-renum.txt', 'r')

    # Read all valid users and create a set
    # Also write all the users as-is to output cascades file
    valid_uids = set()
    for line in fusers:
        uid, uname = line.split(',')
        valid_uids.add( int(uid) )
        fout.write(line)

    # Separator between users and cascades
    if INSERT_AUX_NODES:
        # If auxiliary nodes are to be inserted, more node names need to be added.
        # So, write an incomplete cascade file, and come back to this later.
        ftemp = tempfile.NamedTemporaryFile()
        fcasc = ftemp
        next_node_num = max(valid_uids) + 1
    else:
        fout.write("\n")
        fcasc = fout

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
                if INSERT_AUX_NODES:
                    fcasc.write("%d;%d,1," % (cascade_id, next_node_num))
                    next_node_num += 1
                else:
                    fcasc.write("%d;" % cascade_id)
                # Take lowest value of check-ins for each user
                to_write = ''
                # for _location, _user, _ts in cascade:
                #     to_write += "%d,%d," % (_user, _ts)
                for _user, _ts in dct.items():
                    # to_write += "%d,%.2f," % (_user, float(round(_ts, -3)))
                    day = (_ts - NEW_EPOCH)/(60.0 * 60.0 * 24.0)
                    to_write += "%d,%d," % (_user, int(round(day)))
                fcasc.write('%s\n' % to_write[:-1])
                cascade_id += 1
            else:
                print 'Skipping cascade %d with checkins %d.' % (cascade_id, len(cascade))

            # Begin a new cascade with this location
            cascade = set( [ (location, user, ts_int), ] )
            cur_location = location

    if INSERT_AUX_NODES:
        # Dump the remaining newly created nodes
        for node_num in range(max(valid_uids), next_node_num):
            fout.write("%d,%d\n" % (node_num, node_num))
        fout.write("\n")

        # Copy cascades from the temp file into the cascades file
        fcasc.seek(0)
        for line in fcasc:
            fout.write(line)
        fcasc.close()

    fin.close()
    fout.close()

    # Write ground truth
    if INSERT_AUX_NODES:
        all_uids = valid_uids | set(range(max(valid_uids), next_node_num))
    else:
        all_uids = valid_uids
    for uid in sorted(list(all_uids)):
        fground.write('%d,%d\n' % (uid, uid))
    fground.write('\n')
    for x in sorted(list(all_uids)):
        for y in sorted(list(all_uids)):
            if x != y:
                c_str = '%d,%d,' % (x, y)
                for ts in range(1, TIME_LIMIT, TIME_INT):
                    c_str += '%d,%f,' % (ts, 0.00)
                fground.write(c_str[:-1] + '\n')
                break
    fground.close()


if __name__ == '__main__':
    main()
