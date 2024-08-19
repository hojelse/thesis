import log
from parse_graph import parse_text_to_adj
from medial_graph import medial_graph, medial_graph_2
from carving_decomposition import carving_decomposition

# Construct a branch decomposition of a graph
def branch_decomposition(G_adj: dict[int, list[int]]):
	# Contruct the carving decomposition of the medial graph
	Gx, node_to_vertexpair = medial_graph(G_adj)

	cd = carving_decomposition(Gx.copy())

	# Convert the carving decomposition of M to a branch decomposition of G
	def decomp(t):
		if isinstance(t, int):
			return node_to_vertexpair[t]
		return tuple([decomp(a) for a in t])
	
	bd = decomp(cd)

	log.add("Branch decomposition: " + str(bd))
	return bd

if __name__ == "__main__":
	adj = parse_text_to_adj()
	bd = branch_decomposition(adj)
	print(bd)