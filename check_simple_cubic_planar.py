import matplotlib.pyplot as plt
import networkx as nx
import sys

N, graph_idx = map(int, sys.argv[1:])

G = nx.MultiDiGraph()

with open(f"./graphs/{N}/{N}-{graph_idx}.bin", "rb") as file:
	byte_s = file.read(1)
	N = int.from_bytes(byte_s, byteorder='little')
	
	for i in range(1, N+1):
		G.add_node(i)
	
	for i in range(1, N+1):
		G.add_edge(i, int.from_bytes(file.read(1), byteorder='little'))
		G.add_edge(i, int.from_bytes(file.read(1), byteorder='little'))
		G.add_edge(i, int.from_bytes(file.read(1), byteorder='little'))
		file.read(1)

def is_simple(G):
	for v in G.nodes:
		es = list(G.edges(v))

		# check for self loops
		if (v, v) in es:
			return False

		# check for parallel edges
		e = es[0]
		for e2 in es[1:]:
			if e2 == e:
				return False
			e = e2
	return True

def is_3_regular(G):
	for v in G.nodes:
		xs = list(G[v])
		if len(xs) != 3:
			return False
	return True

print("is simple" if is_simple(G) else "NOT simple")
print("is cubic" if is_3_regular(G) else "NOT cubic")
print("is planar" if nx.is_planar(G) else "NOT planar")

if not (is_simple(G) and is_3_regular(G) and nx.is_planar(G)):
	plt.figure()
	pos = nx.planar_layout(G)
	nx.draw_networkx_nodes(G, pos, node_color = 'r', node_size = 100, alpha = 1)
	nx.draw_networkx_labels(G, pos, font_size=8)
	ax = plt.gca()
	for e in G.edges:
		ax.annotate("",
					xy=pos[e[0]], xycoords='data',
					xytext=pos[e[1]], textcoords='data',
					arrowprops=dict(arrowstyle="->", color="0.5",
									shrinkA=5, shrinkB=5,
									patchA=None, patchB=None,
									connectionstyle="arc3,rad=rrr".replace('rrr',str(0.2*e[2])),
									),
					)
	plt.axis('off')
	plt.show()
