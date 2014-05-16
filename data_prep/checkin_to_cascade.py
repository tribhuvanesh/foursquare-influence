import datetime
import sys
from utils import *
import operator

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
MIN_CHECKINS = 2
NEW_EPOCH = 1262304000


def main(checkins_fn, cascades_fn, users_fn, friendships_fn, no_users_fn):
    fin = open(checkins_fn, 'r')
    fout = open(cascades_fn, 'w')
    fusers = open(users_fn, 'r')
    filename = friendships_fn
    # Read all valid users and create a set
    valid_uids = set()
    for line in fusers:
        uid, uname = line.split(',')
        valid_uids.add(int(uid))
        fout.write(line)

    fout.write("\n")

    # Skip the header
    #fin.readline()
    no_friends = get_unconnected_users(no_users_fn)

    friendships = get_friendship_edges_dict(filename)
    cascades = {}

    for line in fin:
        _user, _latitude, _longitude, _ts, _location = line.split(',')
        location = int(_location)
        user = int(_user)
        if user in no_friends:
            continue
        ts = datetime.datetime.strptime(_ts.strip(), TIME_FORMAT)
        ts_int = int(ts.strftime('%s')) / (3600 * 24)
        current_cascade = cascades.setdefault(location, {})
        current_cascade[user] = min(ts_int, current_cascade.setdefault(user, sys.maxint))
    all_edges = {}
    for cascade in cascades:
        current_cascade = cascades[cascade]
        current_cascade = sorted(current_cascade.iteritems(), key=operator.itemgetter(1))
        #print current_cascade
        if len(current_cascade) > MIN_CHECKINS:
            to_write = []
            for idx, val in enumerate(current_cascade):
                user, time = val
                to_write.append(str(user) + "," + str(time))
                for new_user, time in current_cascade[idx + 1:]:
                    all_edges[(user, new_user)] = all_edges.setdefault((user, new_user), 0) + 1
            fout.write(",".join(to_write) + "\n")
        #break
    print len(all_edges)
    print len(friendships)
    counter = 0
    #print friendships
    for key in all_edges:
        #pass
        #print key
        if key not in friendships:
            counter += 1
    print counter
    fin.close()
    fout.close()


if __name__ == '__main__':
    if len(sys.argv) < 6:
        sys.exit("Format: checkin_to_cascade.py checkins_fn, cascades_fn, users_fn, friendships_fn, no_users_fn")
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
