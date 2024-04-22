from parse_graph import parse_graph_to_adj, adj_to_nx
from medial_graph import medial_graph
import matplotlib.pyplot as plt
import networkx as nx

g_adj = parse_graph_to_adj()
m_adj, node_to_edge, edge_to_node = medial_graph(g_adj)

# increase ids of medial graph nodes
offset = len(g_adj)
m_adj = {f"m{k}": list(map(lambda x: f"m{x}", v)) for k, v in m_adj.items()}

g_nx = adj_to_nx(g_adj)
pos = nx.planar_layout(g_nx)
nx.draw(g_nx, pos, with_labels=True)

m_nx = adj_to_nx(m_adj)
def node_to_pos2(node):
	n = int(node.split('m')[1])
	a,b = node_to_edge[n]
	xa,ya = pos[a]
	xb,yb = pos[b]
	return ((xa+xb)/2, (ya+yb)/2)

pos2 = dict([(k, node_to_pos2(k)) for k in m_adj])
nx.draw(m_nx, pos2, with_labels=True, node_color='g', edge_color='g')

plt.show()