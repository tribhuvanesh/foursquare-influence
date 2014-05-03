'''
Renumbers edges
Input: a) List of friendship edges b) Original checkins file
Output: a) List of renumbered edges (For NetRate and InfoPath) b) Mapping between old and new user IDs
c) Renumbered checkins file
'''

import sys


def main():
    if len(sys.argv) != 3:
        sys.exit("Format: renumber-friendship-edges.py friendship-edges.txt orginal-checkins.txt")

    fname_fedges = sys.argv[1]
    fname_new_fedges = fname_fedges.split('.')[0] + '-renum.txt'
    fname_mapping = fname_fedges.split('.')[0] + '-old-to-new-mapping.txt'
    fname_o_checkins = sys.argv[2]
    fname_new_checkins = fname_o_checkins.split('.')[0] + '-renum.txt'
    fname_users = fname_fedges.split('.')[0] + '-users-renum.txt'

    # First pass - Create mapping between node IDs and new node IDs
    node_id = 1
    nodemap = {}
    added_nodes = set()
    with open(fname_fedges, 'r') as f_fedges, open(fname_new_fedges, 'w') as f_new, open(fname_mapping, 'w') as f_map, \
        open(fname_users, 'w') as f_users:
        for line in f_fedges:
            u1, u2 = map(int, line[:-1].split(','))
            for u in [u1, u2]:
                if u not in added_nodes:
                    added_nodes.add(u)
                    nodemap[u] = node_id
                    f_map.write('%d,%d\n' % (u, node_id))
                    f_users.write('%d,%d\n' % (node_id, node_id))
                    node_id += 1
            f_new.write('%d,%d\n' % (nodemap[u1], nodemap[u2]))

    # Second pass - Renumber checkins
    with open(fname_o_checkins, 'r') as f_chk, open(fname_new_checkins, 'w') as f_new_chk:
        # f_chk.readline() # Skip header
        to_write = []
        for line in f_chk:
            us, lat, lng, tm, loc = line[:-1].split(',')
            if int(us) in added_nodes:
                # f_new_chk.write('%s,%d,%s\n' % (loc, nodemap[int(us)], tm))
                to_write.append( '%s,%d,%s\n' % (loc, nodemap[int(us)], tm) )
        to_write.sort(key=lambda x:int(x.split(',')[0]))
        for line in to_write:
            f_new_chk.write(line)


if __name__ == '__main__':
    main()
