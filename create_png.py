import matplotlib.pyplot as plt
import networkx as nx
import sys

N, graph_idx = map(int, sys.argv[1:])

G = nx.Graph()

with open(f"./graphs/{N}-{graph_idx}.bin", "rb") as file:
	byte_s = file.read(1)
	N = ord(byte_s)
	
	for i in range(1, N+1):
		G.add_node(i)
	
	for i in range(1, N+1):
		G.add_edge(i, ord(file.read(1)))
		G.add_edge(i, ord(file.read(1)))
		G.add_edge(i, ord(file.read(1)))
		file.read(1)

plt.figure()
nx.draw(G, pos=nx.planar_layout(G), with_labels=True)
plt.savefig(f'./graphs/{N}-{graph_idx}.png')
# plt.show()
