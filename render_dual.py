from parse_graph import parse_graph_to_adj, adj_to_nx
from dual_graph import dual_graph
import matplotlib.pyplot as plt
import networkx as nx

g_adj = parse_graph_to_adj()
d_adj, edge_to_link, link_to_edge, node_to_face, face_to_node, edge_to_node = dual_graph(g_adj)

# increase ids of medial graph nodes
offset = len(g_adj)
d_adj = {f"d{k}": list(map(lambda x: f"d{x}", v)) for k, v in d_adj.items()}

print("d_adj", d_adj)

g_nx = adj_to_nx(g_adj)
pos = nx.planar_layout(g_nx)
nx.draw(g_nx, pos, with_labels=True)

m_nx = adj_to_nx(d_adj)
def node_to_pos2(node):
	n = int(node.split('d')[1])
	vertices = list(map(lambda x: x[0], node_to_face[n]))
	poss = [pos[v] for v in vertices]
	center = [sum([p[0] for p in poss])/len(poss), sum([p[1] for p in poss])/len(poss)]
	return center

pos2 = dict([(k, node_to_pos2(k)) for k in d_adj])
nx.draw(m_nx, pos2, with_labels=True, node_color='r', edge_color='r')

plt.show()