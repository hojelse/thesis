import networkx as nx
from util import adj_from_stdin, adj_to_nx

G = adj_to_nx(adj_from_stdin())

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
