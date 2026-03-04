import networkx as nx

G = nx.path_graph(10)
nx.is_tree(G)

# The reason for explicit positioning will become clear in a moment
G = nx.Graph([(0, 1), (1, 2), (1, 3), (3, 4), (3, 5)])
nx.set_node_attributes(
    G, {0: (0, 2), 1: (1, 1), 2: (0, 0), 3: (2, 1), 4: (3, 2), 5: (3, 0)}, "pos"
)

H = nx.Graph([(6, 5), (5, 4), (5, 3), (3, 2), (3, 1)])
nx.set_node_attributes(
    H, {6: (0, 2), 5: (0, 1), 4: (0, 0), 3: (1, 1), 2: (1, 2), 1: (1, 0)}, "pos"
)
nx.set_node_attributes(H, values="tab:red", name="color")
import matplotlib.pyplot as plt

fig, ax = plt.subplots(1, 2, figsize=(12, 6))

for graph, axis in zip((G, H), ax):
    nx.display(graph, canvas=axis)
    axis.set_axis_off()

G = nx.Graph()
G.add_node(0)  # our "root" node

# Then, let's add each of the remaining 9 nodes as leaves connected only to
# the root
G.add_edges_from((0, n) for n in range(1, 10))

fig, ax = plt.subplots()
# Position nodes hierarchically, with "root" on one end and "leaves" on the other
pos = nx.bfs_layout(G, 0, store_pos_as="pos_bfs")

nx.display(G, node_pos="pos_bfs", canvas=ax);
