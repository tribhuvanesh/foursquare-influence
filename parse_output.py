import sys
from gexf import Gexf
from collections import defaultdict


def main():

    if len(sys.argv) != 4:
        sys.exit("Format: parse_output.py infopath-output.txt timesteps.txt timestamp")

    infopath_output_file = sys.argv[1]
    timesteps_file = sys.argv[2]
    ts_to_gen = int(sys.argv[3])
    out_file = "%s-at-%d.gexf" % (infopath_output_file.split('.')[0], ts_to_gen)

    fin = open(infopath_output_file, 'r')
    fts = open(timesteps_file, 'r')
    fout = open(out_file, 'w')


    gexf = Gexf('tribhu_infopath','31-03-2014')
    graph = gexf.addGraph('directed','dynamic','31-03-2014')

    # Add all users as nodes
    for line in fin:
        if ',' not in line: break
        uid, uname = line.split(',')
        uid = int(uid)
        # graph.addNode(str(uid), uname[-1])

    timesteps = map(lambda x: float(x.strip()), fts.readlines())
    first_ts = timesteps[0]
    last_ts = timesteps[-1]

    #
    # Create a dict: timstamp -> [ (source, target, weight), ()...]
    #
    ts_to_edges_dct = defaultdict(list)

    for line in fin:
        vals = map(float, line.split(','))
        source, target = map(int, vals[0:2])
        # Obtain a list of pairs <timestamp, weight>
        edge_weights = [(int(vals[i]), float(vals[i+1])) for i in range(2, len(vals[2:])-1, 2)]

        for ts, weight in edge_weights:
            ts_to_edges_dct[ts] += [(source, target, weight), ]

    # Dump the required timestamps into an output file
    added_nodes = set()
    for source, target, weight in ts_to_edges_dct[ts_to_gen]:
        if source not in added_nodes:
            added_nodes.add(source)
            graph.addNode(str(source), str(source))
        if target not in added_nodes:
            added_nodes.add(target)
            graph.addNode(str(target), str(target))

        edge_id = "%d_to_%d_at_%f" % (source, target, ts)
        graph.addEdge(edge_id, str(source), str(target), weight=weight, label=edge_id)

    gexf.write(fout)


if __name__ == '__main__':
    main()
