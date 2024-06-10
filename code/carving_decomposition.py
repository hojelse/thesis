from carving_width import carving_width
from contraction import contraction
from parse_graph import parse_text_to_adj, adj_to_text
from Graph import Graph

# Find a contraction that does not increase the carving width
def nonincreasing_cw_contraction(G: Graph, cw1: int) -> tuple:
	for es in G.E():
		u, v = G.edge_to_vertexpair[es]
		G2, w = contraction(G, u, v)
		cw2 = carving_width(G2)
		if cw2 <= cw1:
			return G2, (u, v), cw2, w
	return None, None, None, None

# Contract edges that do not increase the carving width
# until only 3 vertices remain.
# Return the resulting graph and the edges that were contracted
def gradient_descent_contractions(G: Graph) -> Graph:
	G2 = G.copy()
	cw1 = carving_width(G)
	edges = dict()
	while True:
		G3, uv, cw2, w = nonincreasing_cw_contraction(G2, cw1)
		if G3 is not None and len(G3.V()) >= 3:
			G2 = G3
			cw1 = cw2
			edges[w] = uv
		if len(G2.V()) == 3:
			return G2, edges

# Contruct a carving decomposition of a graph
def carving_decomposition(G: Graph) -> tuple:
	G2, edges = gradient_descent_contractions(G)

	# Construct the decomposition from the edges that were contracted

	def decomp(x):
		if x not in edges:
			return x
		a,b = edges[x]
		return (decomp(a), decomp(b))

	a,b,c = G2.V()
	cd = (decomp(a), decomp(b), decomp(c))
	return cd

if __name__ == "__main__":
	adj = parse_text_to_adj()
	cd = carving_decomposition(adj)
	print(cd)