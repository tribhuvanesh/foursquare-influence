
# coding: utf-8

# In[2]:

import networkx as nx

from utils import *

# In[3]:

#import matplotlib.pyplot as plt


# In[4]:

import random


# In[5]:

import numpy as np


# In[6]:

#from collections import deque


# In[18]:

NUM_CASCADES = 200


# In[8]:

WALK_LEN = 10


# In[9]:

TIME_LIMIT = 5
#TIME_LIMIT = 100


# In[10]:

#ffr = open('small_graph.txt', 'r')

ffr = open('only_zurich_friendship.out', 'r')

# In[19]:

fout = open('synth-cascades-zurich-complete.txt', 'w')


fgr = open('ground_truth.txt', 'w')

# In[12]:

added_nodes = set()


# In[13]:

G = nx.DiGraph()


# In[14]:

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
    fgr.write(str(edge[0]) + " " + str(edge[1]) + " " + str(edge_labels[edge]) + "\n")

fgr.close()
# In[20]:

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

    #fout.write("%d;" % i)
    i += 1
    cascade.sort(key=lambda tup: tup[1])
    cascade_str_array = []
    for elem in cascade:
        cascade_str_array.append(str(elem[0]) + "," + str(elem[1]))
    fout.write(",".join(cascade_str_array) + "\n")
fout.close()
