'''
Renumbers edges
Input: List of friendship edges
Output: a) List of renumbered edges (For NetRate and InfoPath) b) Mapping between old and new user IDs
'''

import sys


def main():
    if len(sys.argv) != 2:
        sys.exit("Format: renumber-friendship-edges.py friendship-edges.txt")

    fname_fedges = sys.argv[1]
    fname_new_fedges = fname_fedges.split('.')[0] + '-renum.txt'
    fname_mapping = fname_fedges.split('.')[0] + '-old-to-new-mapping.txt'

    # First pass - Create mapping between node IDs and new node IDs
    node_id = 0
    nodemap = {}
    added_nodes = set()
    with open(fname_fedges, 'r') as f_fedges, open(fname_new_fedges, 'w') as f_new, open(fname_mapping, 'w') as f_map:
        for line in f_fedges:
            u1, u2 = map(int, line[:-1].split(','))
            for u in [u1, u2]:
                if u not in added_nodes:
                    added_nodes.add(u)
                    nodemap[u] = node_id
                    f_map.write('%d,%d\n' % (u, node_id))
                    node_id += 1
            f_new.write('%d,%d\n' % (nodemap[u1], nodemap[u2]))


if __name__ == '__main__':
    main()
