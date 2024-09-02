from typing import Union
from Graph import Graph, read_lmg_from_stdin
from medial_graph import medial_graph
from carving_decomposition import carving_decomposition
from util import adj_from_stdin, adj_to_str

def carving_decomposition_to_branch_decomposition(
	cd: dict[int, list[int]],
	node_to_vertexpair: dict[int, tuple[int, int]]
) -> dict[int, list[Union[int, tuple[int, int]]]]:

	leafs = [u for u,vs in cd.items() if len(vs) == 1]

	bd = dict()
	for u,vs in cd.items():
		bd[u if u not in leafs else node_to_vertexpair[u]] = [v if v not in leafs else node_to_vertexpair[v] for v in vs]

	return bd

# Construct a branch decomposition of a graph
def branch_decomposition(G: Graph) -> dict[int, list[Union[int, tuple[int, int]]]]:
	Gx, node_to_vertexpair = medial_graph(G)
	cd = carving_decomposition(Gx.copy())
	bd = carving_decomposition_to_branch_decomposition(cd, node_to_vertexpair)
	return bd

if __name__ == "__main__":
	# Uncomment for multigraphs
	# G = Graph()
	# G.from_lmg(read_lmg_from_stdin())
	# bd = branch_decomposition(G)
	# print("bd", bd)

	adj = adj_from_stdin()
	G = Graph()
	G.from_adj(adj)
	bd = branch_decomposition(G)
	print(adj_to_str(bd))