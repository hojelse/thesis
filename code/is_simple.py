import networkx as nx
from parse_graph import parse_text_to_adj, adj_to_nx

G = adj_to_nx(parse_text_to_adj())

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

print(is_simple(G))
