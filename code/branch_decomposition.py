from parse_graph import parse_text_to_adj
from medial_graph import medial_graph
from carving_decomposition import carving_decomposition

# Construct a branch decomposition of a graph
def branch_decomposition(G_adj: dict[int, list[int]]):
	# Contruct the carving decomposition of the medial graph
	M, node_to_vertexpair, vertexpair_to_node = medial_graph(G_adj)
	cd = carving_decomposition(M)

	# Convert the carving decomposition of M to a branch decomposition of G

	def decomp(t):
		if isinstance(t, int):
			return node_to_vertexpair[t]
		return tuple([decomp(a) for a in t])
	
	bd = decomp(cd)
	return bd

if __name__ == "__main__":
	adj = parse_text_to_adj()
	bd = branch_decomposition(adj)
	print(bd)