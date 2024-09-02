from typing import Union
from Graph import Graph
from branch_decomposition import branch_decomposition
from util import adj_from_stdin

def branch_width_of_branch_decomposition(bd: dict[int, list[Union[int, tuple[int, int]]]]) -> int:
	# Get the vertex set of the leafs of the subtree of x (not y)
	def leafs_set(x, y):
		leafs = set()
		visited = set([y])
		stack = [x]
		while stack:
			v = stack.pop()
			if isinstance(v, tuple):
				leafs.update(set(v))
				continue
			if v not in visited:
				visited.add(v)
				for w in bd[v]:
					stack.append(w)
		return leafs

	# Find the maximal width of any middle set
	width = 0
	for x,ys in bd.items():
		for y in ys:
			a = leafs_set(x, y)
			b = leafs_set(y, x)
			middle_set = len(a.intersection(b))
			width = max(width, middle_set)

	return width

def branch_width(G: Graph) -> int:
	bd = branch_decomposition(G)
	bw = branch_width_of_branch_decomposition(bd)

	return bw

if __name__ == "__main__":
	# Uncomment for multigraphs
	# G = Graph()
	# G.from_lmg(read_lmg_from_stdin())
	# bw = branch_width(G)
	# print("bw", bw)

	adj = adj_from_stdin()
	G = Graph()
	G.from_adj(adj)
	bw = branch_width(G)
	print(bw)
