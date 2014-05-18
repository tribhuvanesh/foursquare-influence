import networkx as nx
from data_prep.utils import *
import random
import numpy as np
import sys
import tempfile


# NUM_CASCADES = 200
WALK_LEN = 10
TIME_LIMIT = 15
INFOPATH_FORMAT = True
INSERT_AUX_NODES = False
REPEAT_NUM = 1
GEN_FULL = True # Setting this to True will generate infections over all edges, otherwise with prob. MIX_PERC
MIX_PERC = 0.5

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
            G.add_edge(u1, u2, weight=np.random.uniform(0.05, 2.00))
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

    # Write all the nodes to cascades file
    for uid in sorted(added_nodes):
        fout.write("%s,%s\n" % (uid, uid))

    if INSERT_AUX_NODES:
        # If auxiliary nodes are to be inserted, more node names need to be added.
        # So, write an incomplete cascade file, and come back to this later.
        ftemp = tempfile.NamedTemporaryFile()
        fcasc = ftemp
        next_node_num = max(added_nodes) + 1
    else:
        fout.write("\n")
        fcasc = fout

    i = 0
    for xyz in range(REPEAT_NUM):
        cascade_edge_count = {}
        for edge in G.edges():
            cascade_edge_count[edge] = 0
        # Continue generating if there exists even a single edge without an infection
        gen_more_1 = lambda ecount_dct : 0 in ecount_dct.values()
        # Continue infecting, until 75% of the edges have an infection
        gen_more_2 = lambda ecount_dct : (ecount_dct.values().count(0) / float(len(ecount_dct))) > MIX_PERC
        gen_more = (gen_more_2, gen_more_1)[int(GEN_FULL)]
        while gen_more(cascade_edge_count):
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
                    # activation_time = int(np.ceil(cur_time + np.random.power(trans_rate)))
                    # activation_time = int(np.ceil(cur_time + np.random.rayleigh(1.0/trans_rate)))
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
                fcasc.write("%d;" % i)
            i += 1
            cascade.sort(key=lambda tup: tup[1])

            if INSERT_AUX_NODES:
                cascade_str_array = ['%d,%d' % (next_node_num, 1), ]
                next_node_num += 1
            else:
                cascade_str_array = []

            for elem in cascade:
                cascade_str_array.append(str(elem[0]) + "," + str(elem[1]))
            fcasc.write(",".join(cascade_str_array) + "\n")

    if INSERT_AUX_NODES:
        # Dump the remaining newly created nodes
        for node_num in range(max(added_nodes), next_node_num):
            fout.write("%d,%d\n" % (node_num, node_num))
        fout.write("\n")

        # Copy cascades from the temp file into the cascades file
        fcasc.seek(0)
        for line in fcasc:
            fout.write(line)
        fcasc.close()

    fout.close()

    if INFOPATH_FORMAT:
        if INSERT_AUX_NODES:
            added_nodes_all = added_nodes | set(range(max(added_nodes), next_node_num))
        else:
            added_nodes_all = added_nodes
        for uid in sorted(list(added_nodes_all)):
            fgr_c.write('%d,%d\n' % (uid, uid))
        fgr_c.write('\n')
        # Write cartesian product
        # all_pairs = [(x, y) for y for x in sorted(list(added_nodes))]
        for x in sorted(list(added_nodes_all)):
            for y in sorted(list(added_nodes_all)):
                if x != y:
                    c_str = '%d,%d,' % (x, y)
                    for ts in range(TIME_LIMIT):
                        c_str += '%d,%f,' % (ts, 0.00)
                    fgr_c.write(c_str[:-1] + '\n')
            break
    fgr_c.close()


if __name__ == '__main__':
    main()
