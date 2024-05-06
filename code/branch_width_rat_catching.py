from parse_graph import parse_text_to_adj, adj_to_text
from medial_graph import medial_graph
from carving_width_rat_catching import carving_width_rat_catching
from contraction import contraction

def valid_contraction(G, cw1):
	for x,ys in G.items():
		for y in ys:
			if x < y:
				G2, z = contraction(G, (x, y))
				cw2 = carving_width_rat_catching(G2)
				if cw2 <= cw1:
					return G2, (x, y), cw2, z
	return None, None, None, None

def gradient_descent(G):
	cw = carving_width_rat_catching(G)
	edges = dict()
	while True:
		G2, e, cw2, z = valid_contraction(G, cw)
		if G2 is not None and len(G2) >= 3:
			G = G2
			cw = cw2
			edges[z] = e
		if len(G) == 3:
			return G, edges

def carving_decomposition(G):
	G2, edges = gradient_descent(G)

	def decomp(x):
		if x not in edges:
			return x
		a,b = edges[x]
		return (decomp(a), decomp(b))

	print(edges)
	a,b,c = G2.keys()
	cd = (decomp(a), decomp(b), decomp(c))
	return cd

def branch_decomposition(G):
	M, node_to_edge, edge_to_node = medial_graph(G)
	cd = carving_decomposition(M)

	def decomp(x):
		if isinstance(x, int):
			return node_to_edge[x]
		return tuple([decomp(a) for a in x])
	
	bd = decomp(cd)
	return bd

if __name__ == "__main__":
	G = parse_text_to_adj()
	print(branch_decomposition(G))

# edges
# newick_format
# newick_format -> branch_width