import matplotlib.pyplot as plt
import networkx as nx
import sys
from code.parse_graph import parse_graph_to_nx

G = parse_graph_to_nx()

plt.figure()
if nx.is_planar(G):
	nx.draw(G, pos=nx.planar_layout(G), with_labels=True)
else:
	nx.draw(G, with_labels=True)
plt.savefig(sys.stdout.buffer)
# plt.show()
