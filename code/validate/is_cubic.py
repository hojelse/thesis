import networkx as nx
from util import adj_from_stdin, adj_to_nx

G = adj_to_nx(adj_from_stdin())

def is_3_regular(G):
	for v in G.nodes:
		xs = list(G[v])
		if len(xs) != 3:
			return False
	return True

print(is_3_regular(G))
