from parse_graph import parse_text_to_adj, adj_to_text

class Graph:
	def __init__(self):
		self.adj_edges: dict[int, list[int]] = dict()
		self.edge_to_vertexpair: dict[int, tuple[int, int]] = dict()
		pass

	def from_adj(self, adj: dict[int, list[int]]):
		# assign edge ids
		self.adj_edges = adj.copy()
		next_edgeid = 1
		for x, ys in self.adj_edges.items():
			for i,y in enumerate(ys):
				if x < y:
					self.edge_to_vertexpair[next_edgeid] = (x, y)
					self.edge_to_vertexpair[-next_edgeid] = (y, x)
					
					self.adj_edges[x][i] = next_edgeid
					self.adj_edges[y][adj[y].index(x)] = -next_edgeid

					next_edgeid += 1

	def incident_edges(self, v: int) -> list[int]:
		return self.adj_edges[v]

	def V(self) -> list[int]:
		return list(self.adj_edges.keys())
	
	def E(self) -> list[int]:
		return list(self.edge_to_vertexpair.keys())

	def N(self, v: int) -> list[int]:
		return [self.edge_to_vertexpair[e][1] for e in self.adj_edges[v]]

	def adj(self) -> dict[int, list[int]]:
		return dict([(x, self.N(x)) for x in self.adj_edges.keys()])
	
	def copy(self):
		H = Graph()
		H.adj_edges = self.adj_edges.copy()
		H.edge_to_vertexpair = self.edge_to_vertexpair.copy()
		return H

def dual_graph(G: Graph) -> Graph:
	edges = [e for e in G.E()]

	D = Graph()
	edge_to_link = dict()
	link_to_edge = dict()
	node_to_face = dict()
	edge_to_node = dict()

	next_nodeid = 1
	while edges:
		e = edges.pop()
		next_e = e
		edge_to_node[e] = next_nodeid
		face = [e]
		while True:
			# print("face", face, list(map(lambda x: G.edge_to_vertexpair[x], face)))
			u,v = G.edge_to_vertexpair[next_e]
			idx = G.adj_edges[v].index(-next_e)
			next_e = G.adj_edges[v][(idx-1)%len(G.adj_edges[v])]
			if (next_e == e):
				break
			# print("next_e", next_e)
			edges.remove(next_e)
			face.append(next_e)
			edge_to_node[next_e] = next_nodeid
		node_to_face[next_nodeid] = face
		next_nodeid += 1

	for i in node_to_face.keys():
		D.adj_edges[i] = []

	next_linkid = 1
	for i,f1 in node_to_face.items():
		for j,f2 in node_to_face.items():
			if i < j:
				common_edges = set(list(map(abs, f1))).intersection(set(map(abs, f2)))
				for e in common_edges:
					D.edge_to_vertexpair[next_linkid] = (i, j)
					D.edge_to_vertexpair[-next_linkid] = (j, i)
					edge_to_link[e] = next_linkid
					link_to_edge[next_linkid] = e
					edge_to_link[-e] = -next_linkid
					link_to_edge[-next_linkid] = -e
					D.adj_edges[i].append(next_linkid)
					D.adj_edges[j].append(-next_linkid)
					next_linkid += 1

	return D, edge_to_link, link_to_edge, node_to_face, edge_to_node

import math

def carving_width(G: Graph) -> int:
	D, edge_to_link, link_to_edge, node_to_face, edge_to_node = dual_graph(G)

	# When the rat-catcher is on edge e, edge f is noisy iff there is
	# a closed walk of at most length k containing e* and f* in G* .
	# Return the un-noisy subgraph.
	def noisy_links(l: int, k: int) -> set[int]:
		s,t = D.edge_to_vertexpair[l]
		links = link_to_edge.keys()

		def dists(n: int) -> dict[int, int]:
			dist = {v: -1 for v in D.V()}
			dist[n] = 0
			stack = [n]
			while len(stack) > 0:
				v = stack.pop()
				for y in D.N(v):
					if dist[y] == -1:
						dist[y] = dist[v] + 1
						stack.append(y)
			return dist
		
		dist_s = dists(s)
		dist_t = dists(t)

		noisy = []
		for l in links:
			u,v = D.edge_to_vertexpair[l]
			if dist_s[u] + dist_t[v] + 2 < k:
				noisy.append(l)

		return set([abs(e) for e in noisy])

	def quiet_links(l: int, k: int) -> set[int]:
		links = set([abs(e) for e in D.E()])
		return links - noisy_links(l, k)

	def quiet_edges(e: int, k: int) -> set[int]:
		return set([abs(link_to_edge[l]) for l in quiet_links(edge_to_link[e], k)])

	def quiet_components(e: int, k: int) -> dict[int, list[int]]:
		edges = quiet_edges(e, k)

		quiet_subgraph = {v: [] for v in G.V()}
		for e in edges:
			u,v = G.edge_to_vertexpair[e]
			quiet_subgraph[u].append(e)
			quiet_subgraph[v].append(-e)

		components = []
		unseen = set(quiet_subgraph.keys())

		while len(unseen) > 0:
			v = unseen.pop()
			component = [v]
			stack = [v]
			while len(stack) > 0:
				v = stack.pop()
				for e in quiet_subgraph[v]:
					u,v = G.edge_to_vertexpair[e]
					if v in unseen:
						unseen.remove(v)
						stack.append(v)
						component.append(v)
			components.append(component)

		return components

	def flatten(xss):
		return set([x for xs in xss for x in xs])

	# Assume |V(G)| >= 2
	# Return True
	# iff. carving-width >= k
	# iff. rat has a winning escape strategy with noise-level k
	def rat_wins(k: int) -> bool:
		if len(G.V()) < 2:
			return False
		
		if max([len(G.N(v)) for v in G.V()]) >= k:
			return True

		edge_set = edge_to_link.keys()

		Te = set([(e, tuple(C)) for e in edge_set for C in quiet_components(e, k)])
		Sr = set([(r, v) for r in node_to_face.keys() for v in G.V()])

		losing_eC = set()
		losing_rv = set()

		for (r, v) in Sr:
			if v in flatten([G.edge_to_vertexpair[e] for e in node_to_face[r]]):
				losing_rv.add((r,v))

		if len(Te) == len(losing_eC) or len(Sr) == len(losing_rv):
			return False

		while True:
			new_deletion = False

			for (e, C) in Te:
				if all([(edge_to_node[e], v) in losing_rv for v in C]):
					if (e, C) not in losing_eC:
						new_deletion = True
						losing_eC.add((e, C))
			
			for (e, C) in losing_eC:
				r1 = edge_to_node[e]
				r2 = edge_to_node[-e]
				for (r, v) in [(r1, v) for v in C] + [(r2, v) for v in C]:
					if (r, v) not in losing_rv:
						new_deletion = True
						losing_rv.add((r, v))

			if len(Te) == len(losing_eC) or len(Sr) == len(losing_rv):
				return False
			elif not new_deletion:
				return True
			
	def binary_search_cw():
		l = 0
		r = 1
		while True:
			if rat_wins(r):
				l = r
				r *= 2
			else:
				break
		m = l
		while l < r:
			m = int(math.ceil((l + r) / 2))
			if rat_wins(m):
				l = m
			else:
				r = m - 1
		return l
	
	cw = binary_search_cw()
	return cw

def index_of_first(lst, pred):
	for i, v in enumerate(lst):
		if pred(v):
			return i
	return None

def contraction(G: Graph, a: int, b: int) -> Graph:
	# copy G
	G1 = G.copy()

	c = max(G1.adj_edges.keys()) + 1

	# let every edge incident to a or b be incident to c instead
	for e in G1.E():
		u,v = G1.edge_to_vertexpair[e]
		if u == a or u == b:
			G1.edge_to_vertexpair[e] = (c, v)
		u,v = G1.edge_to_vertexpair[e]
		if v == a or v == b:
			G1.edge_to_vertexpair[e] = (u, c)

	# create neighborhood of c
	first_shared_edge = G1.adj_edges[a][index_of_first(G1.adj_edges[a], lambda e: G1.edge_to_vertexpair[e][0] == c and G1.edge_to_vertexpair[e][1] == c)]

	idx1 = G1.adj_edges[a].index(first_shared_edge)
	rotated_Ga = G1.adj_edges[a][idx1:] + G1.adj_edges[a][:idx1]

	idx2 = G1.adj_edges[b].index(-first_shared_edge)
	rotated_Gb = G1.adj_edges[b][idx2:] + G1.adj_edges[b][:idx2]

	G1.adj_edges[c] = rotated_Ga + rotated_Gb

	# remove c <-> c edges
	G1.adj_edges[c] = [e for e in G1.adj_edges[c] if not (G1.edge_to_vertexpair[e][0] == G1.edge_to_vertexpair[e][1] == c)]
	G1.edge_to_vertexpair = dict([(k,v) for k,v in G1.edge_to_vertexpair.items() if not (v[0] == v[1] == c)])

	# remove a and b
	del G1.adj_edges[a]
	del G1.adj_edges[b]

	return G1, c

# Find a contraction that does not increase the carving width
def nonincreasing_cw_contraction(G: Graph, cw1):
	for x,ys in G.adj().items():
		for y in ys:
			if x < y:
				# print("G.adj_edges", G.adj_edges)
				# print("G.edge_to_vertexpair", G.edge_to_vertexpair)
				# print("contracting", x, y)
				G2, z = contraction(G, x, y)
				# print("G2.adj_edges", G2.adj_edges)
				# print("G2.edge_to_vertexpair", G2.edge_to_vertexpair)
				# print("new vertex", z)
				cw2 = carving_width(G2)
				if cw2 <= cw1:
					return G2, (x, y), cw2, z
	return None, None, None, None

# Contract edges that do not increase the carving width
# until only 3 vertices remain
def gradient_descent_contractions(G: Graph) -> Graph:
	G2 = G.copy()
	cw1 = carving_width(G)
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

def medial_graph(adj: dict[int, list[int]]) -> Graph:
	es = set([tuple(sorted((i, j))) for i in adj for j in adj[i]])

	vertexpair_to_node = dict([(e, i+1) for i,e in enumerate(es)])
	node_to_vertexpair = dict([(i+1, e) for i,e in enumerate(es)])

	medial = dict([(i+1, []) for i in range(len(es))])

	for v,xs in adj.items():
		nodes = [vertexpair_to_node[tuple(sorted((v, x)))] for x in xs]
		for i in range(len(nodes)):
			medial[nodes[i]].append(nodes[(i-1)%len(nodes)])
			medial[nodes[i]].append(nodes[(i+1)%len(nodes)])

	M = Graph()
	M.from_adj(medial)
	return M, node_to_vertexpair, vertexpair_to_node

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

	print(branch_width(adj))
	pass