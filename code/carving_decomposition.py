from collections import defaultdict
from typing import Union
from carving_width import carving_width
from contraction import contraction
from Graph import Graph, read_lmg_from_stdin

# Find a contraction that does not increase the carving width
def nonincreasing_cw_contraction(G: Graph, cw1: int) -> Union[tuple[Graph, tuple[int, int], int, int], None]:
	for e in G.E():
		u, v = G.edge_to_vertexpair[e]
		if u == v:
			continue
		G2, w = contraction(G, u, v)
		cw2 = carving_width(G2)
		if cw2 <= cw1:
			return G2, (u, v), cw2, w
	return None

# Contract edges that do not increase the carving width
# until only 3 vertices remain.
# Return the resulting graph and the edges that were contracted
def gradient_descent_contractions(G: Graph) -> tuple[Graph, dict[int, tuple[int, int]]]:
	G2 = G.copy()
	cw1 = carving_width(G)
	edges = dict()
	while True:
		if len(G2.V()) <= 3:
			return G2, edges
		res = nonincreasing_cw_contraction(G2, cw1)
		if res is not None:
			G3, uv, cw2, w = res
			if len(G3.V()) >= 3:
				G2 = G3
				cw1 = cw2
				edges[w] = uv

# Contruct a carving decomposition of a graph
def carving_decomposition(G: Graph) -> dict[int, list[int]]:
	G2, edges = gradient_descent_contractions(G)

	cd = defaultdict(list)

	# return trivial carving decompositions
	if len(G2.V()) == 1:
		cd[G2.V()[0]] = []
		return cd

	if len(G2.V()) == 2:
		a,b = G2.V()
		cd[a].append(b)
		cd[b].append(a)
		return cd

	# connect the 3 vertices to a new internal vertex and expand
	a,b,c = G2.V()
	d = max(list(edges.keys()) + G2.V()) + 1
	cd[d] = [a,b,c]
	cd[a].append(d)
	cd[b].append(d)
	cd[c].append(d)

	def expand(v):
		if v in edges:
			a,b = edges[v]
			cd[v].append(a)
			cd[v].append(b)
			cd[a].append(v)
			cd[b].append(v)
			if a in edges:
				expand(a)
			if b in edges:
				expand(b)

	for v in G2.V():
		expand(v)

	cd = dict(cd)

	return cd

if __name__ == "__main__":
	G = Graph()
	G.from_lmg(read_lmg_from_stdin())
	cd = carving_decomposition(G)
	print(cd)