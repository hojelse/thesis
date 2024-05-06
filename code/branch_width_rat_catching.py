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

def branch_width(bd):
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

if __name__ == "__main__":
	G = parse_text_to_adj()
	bd = branch_decomposition(G)
	print(bd)
	bw = branch_width(bd)
	print(bw)
