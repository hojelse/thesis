from carving_width import carving_width
from contraction import contraction
from parse_graph import parse_text_to_adj, adj_to_text
from dual_graph import dual_graph
from medial_graph import medial_graph
from Graph import Graph

# Find a contraction that does not increase the carving width
def nonincreasing_cw_contraction(G: Graph, cw1):
	for x,ys in G.adj().items():
		for y in ys:
			if x < y:
				G2, z = contraction(G, x, y)
				cw2 = carving_width(G2)
				if cw2 <= cw1:
					return G2, (x, y), cw2, z
	return None, None, None, None

# Contract edges that do not increase the carving width
# until only 3 vertices remain
def gradient_descent_contractions(G: Graph) -> Graph:
	G2 = G.copy()
	cw1 = carving_width(G)
	# print("cw1", cw1)
	# exit()
	edges = dict()
	while True:
		G3, e, cw2, z = nonincreasing_cw_contraction(G2, cw1)
		if G3 is not None and len(G3.V()) >= 3:
			G2 = G3
			cw1 = cw2
			edges[z] = e
		if len(G2.V()) == 3:
			return G2, edges

def carving_decomposition(G: Graph) -> tuple:
	G2, edges = gradient_descent_contractions(G)

	def decomp(x):
		if x not in edges:
			return x
		a,b = edges[x]
		return (decomp(a), decomp(b))

	a,b,c = G2.V()
	cd = (decomp(a), decomp(b), decomp(c))
	return cd

def branch_decomposition(adj: dict[int, list[int]]):
	M, node_to_vertexpair, vertexpair_to_node = medial_graph(adj)
	cd = carving_decomposition(M)

	def decomp(x):
		if isinstance(x, int):
			return node_to_vertexpair[x]
		return tuple([decomp(a) for a in x])
	
	bd = decomp(cd)
	return bd

def branch_width_of_branch_decomposition(bd):
	t = dict()

	def aux(subtree, depth, name):
		if len(subtree) == 2 and isinstance(subtree[0], int) and isinstance(subtree[1], int):
			t[subtree] = []
			return subtree
		else:
			t[name] = []
			for i,a in enumerate(subtree):
				child_name = aux(a, depth+1, name+str(i))
				t[name].append(child_name)
				t[child_name].append(name)
			return name

	aux(bd, 0, "i0")

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
				for w in t[v]:
					stack.append(w)
		return leafs

	width = 0
	for x,ys in t.items():
		for y in ys:
			a = leafs_set(x, y)
			b = leafs_set(y, x)
			width = max(width, len(a.intersection(b)))
	
	return width

def branch_width(adj: dict[int, list[int]]):
	bd = branch_decomposition(adj)
	return branch_width_of_branch_decomposition(bd)

if __name__ == "__main__":
	adj = parse_text_to_adj()

	bd = branch_decomposition(adj)
	bw = branch_width_of_branch_decomposition(bd)
	print("bw", bw)
	print("bd", bd)
