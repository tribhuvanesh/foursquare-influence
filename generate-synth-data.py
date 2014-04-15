import networkx as nx
from data_prep.utils import *
import random
import numpy as np
import sys


# NUM_CASCADES = 200
WALK_LEN = 10
TIME_LIMIT = 15
INFOPATH_FORMAT = True

def main():
    if len(sys.argv) != 3:
        sys.exit("Format: generate-synth-data.py friendship-edges.txt outfile")

    fname_fedges = sys.argv[1]
    outfile_name = sys.argv[2]
    fname_casc = outfile_name + '-cascades.txt'
    fname_ground = outfile_name + '-ground-truth.txt'
    fname_ground_casc = outfile_name + '-ground-truth-cascade.txt'

    ffr = open(fname_fedges, 'r')
    fout = open(fname_casc, 'w')
    fgr = open(fname_ground, 'w')
    fgr_c = open(fname_ground_casc, 'w')

    added_nodes = set()
    G = nx.DiGraph()

    for line in ffr:
        try:
            u1, u2 = map(int, line[:-1].split(','))
            for u in [u1, u2]:
                if u not in added_nodes:
                    added_nodes.add(u)
                    G.add_node(u)
            G.add_edge(u1, u2, weight=np.random.uniform(0.01, 1))
        except ValueError:
            print line

    #G = nx.read_gexf("synth-cascades-zurich-fig2.gexf")
    #added_nodes = list(G.nodes())
    pos = nx.spring_layout(G)
    nx.draw_networkx_edges(G, pos)
    edge_labels = dict([((u, v,), d['weight']) for u, v, d in G.edges(data=True)])
    #nx.draw_networkx_labels(G, pos, edge_labels=edge_labels)
    #plt.show()
    for edge in edge_labels:
        fgr.write(str(edge[0]) + "," + str(edge[1]) + "," + str(edge_labels[edge]) + "\n")
    fgr.close()

    if INFOPATH_FORMAT:
        for uid in sorted(list(added_nodes)):
            fgr_c.write('%d,%d\n' % (uid, uid))
        fgr_c.write('\n')
        for edge in edge_labels:
            c_str = '%d,%d,' % (edge[0], edge[1])
            for ts in range(TIME_LIMIT):
                c_str += '%d,%f,' % (ts, edge_labels[edge])
            fgr_c.write(c_str[:-1] + '\n')
    fgr_c.close()

    # Write all the nodes to cascades file
    for uid in sorted(added_nodes):
        fout.write("%s,%s\n" % (uid, uid))
    fout.write("\n")

    cascade_edge_count = {}
    for edge in G.edges():
        cascade_edge_count[edge] = 0
    i = 0
    while 0 in [cascade_edge_count[key] for key in cascade_edge_count]:
        # Pick a random node and start a random walk of length walk_len, with memory
        start_node = random.sample(added_nodes, 1)[0]
        visited_nodes = set()
        start_time = 1
        cutoff_time = TIME_LIMIT
        cur_time = start_time
        visit_str = ""
        s = list()
        s.append(start_node)
        depth = {}
        activation = {}
        #Change this line to random
        activation[start_node] = start_time
        depth[start_node] = 0
        cascade = []
        while (len(s) != 0):
            cur_node = s.pop()
            if depth[cur_node] > WALK_LEN:
                continue
            cur_time = activation[cur_node]
            for neighbor in set(G.neighbors(cur_node)):
                trans_rate = G.get_edge_data(cur_node, neighbor)['weight']
                activation_time = int(np.ceil(cur_time + np.random.exponential(1.0 / trans_rate)))
                if neighbor not in activation or activation_time < activation[neighbor]:
                    activation[neighbor] = activation_time
                depth[neighbor] = depth[cur_node] + 1
                if activation_time <= cutoff_time:
                    cascade_edge_count[(cur_node, neighbor)] += 1
                s.append(neighbor)
        for node in activation:
            if activation[node] <= cutoff_time:
                cascade.append((node, activation[node]))
        if len(cascade) == 1:
            continue

        if INFOPATH_FORMAT:
            fout.write("%d;" % i)
        i += 1
        cascade.sort(key=lambda tup: tup[1])
        cascade_str_array = []
        for elem in cascade:
            cascade_str_array.append(str(elem[0]) + "," + str(elem[1]))
        fout.write(",".join(cascade_str_array) + "\n")
    fout.close()


if __name__ == '__main__':
    main()
