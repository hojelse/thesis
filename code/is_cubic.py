import networkx as nx
from parse_graph import parse_text_to_adj, adj_to_nx

G = adj_to_nx(parse_text_to_adj())

def is_3_regular(G):
	for v in G.nodes:
		xs = list(G[v])
		if len(xs) != 3:
			return False
	return True

print(is_3_regular(G))
