
# coding: utf-8

# In[3]:

import networkx as nx


# In[13]:

import matplotlib.pyplot as plt
import numpy as np
# In[14]:

import random
import sys

# In[52]:

NUM_CASCADES = 500


# In[53]:

WALK_LEN = 6


# In[43]:

ffr = open('only_zurich_friendship.out', 'r')


# In[50]:

fout = open('synth-cascades-zurich-1.txt', 'w')


# In[5]:

added_nodes = set()


# In[6]:

G = nx.DiGraph()


# In[7]:

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


# In[41]:
pos = nx.spring_layout(G)
nx.draw_networkx_edges(G, pos)

edge_labels = dict([((u, v,), d['weight']) for u, v, d in G.edges(data=True)])
nx.draw_networkx_labels(G, pos, edge_labels=edge_labels)

# In[42]:

if False:
    plt.show()
    sys.exit(0)

# In[17]:

random.choice(list(added_nodes))


# In[51]:

# Write all the nodes to cascades file
for uid in sorted(list(added_nodes)):
    fout.write("%d,%d\n" % (uid, uid))
fout.write("\n")


# In[54]:

for i in range(NUM_CASCADES):
    # Pick a random node and start a random walk of length walk_len, with memory
    start_node = random.sample(added_nodes, 1)[0]
    visited_nodes = set()
    start_time = random.randint(0, 250)
    cutoff_time = random.randint(start_time, 300)
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

        for neighbor in set(G.neighbors(cur_node)):
            weight = G.get_edge_data(cur_node, neighbor)['weight']
            activation_time = activation[cur_node] + int((2 - weight) * 10)  # Change this to random
            if neighbor not in activation or activation_time < activation[neighbor]:
                activation[neighbor] = activation_time
            depth[neighbor] = depth[cur_node] + 1
            s.append(neighbor)
    for node in activation:
        if activation[node] <= cutoff_time:
            cascade.append((node, activation[node]))
    if len(cascade) == 1:
        continue

    fout.write("%d;" % i)
    cascade.sort(key=lambda tup: tup[1])
    cascade_str_array = []
    for elem in cascade:
        cascade_str_array.append(str(elem[0]) + "," + str(elem[1]))
    #for j in range(WALK_LEN):
    #    print cur_node, "->",
    #    visit_str += "%d,%d," % (cur_node, cur_time)
    #    # Pick a random unvisited neighbour
    #    for neighbour in set(G.neighbors(cur_node)):
    #    visited_nodes.add(cur_node)
    #    try:
    #        next_node = random.sample(cur_neighbours - visited_nodes, 1)[0]
    #        edgeData = G.get_edge_data(cur_node, next_node)
    #        print edgeData['weight']
    #        cur_node = next_node
    #        cur_time += 1
    #    except ValueError:
    #        break  # End the walk. No more unvisited nodes to traverse
    fout.write(",".join(cascade_str_array) + "\n")
    #print "END"


# In[55]:

fout.close()


# In[ ]:
