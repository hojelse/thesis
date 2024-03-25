from parse_graph import parse_graph_to_adj, adj_to_bytes
import math

G = parse_graph_to_adj()

# assume planar graph
# assume clockwise or counterclockwise ordering
def find_faces(adj: dict[int, list[int]]) -> list[list[tuple[int, int]]]:
	edges = set([(i, j) for i in adj for j in adj[i]])
	faces = []
	while len(edges) > 0:
		first_edge = edges.pop()
		v = first_edge[1]
		face = [first_edge]
		next_edge = first_edge
		while True:
			u = adj[next_edge[1]][(adj[next_edge[1]].index(next_edge[0])-1)%len(adj[next_edge[1]])]
			next_edge = (v, u)
			if next_edge == first_edge:
				faces.append(face)
				break
			edges.remove(next_edge)
			face.append(next_edge)
			v = u
	return faces

# Assume planar and clockwise ordering
def medial_graph(G: dict[int, list[int]]):
	es = set([tuple(sorted((i, j))) for i in G for j in G[i]])

	edge_to_node = dict([(e, i+1) for i,e in enumerate(es)])

	M = dict([(i+1, []) for i in range(len(es))])

	for v,xs in G.items():
		nodes = [edge_to_node[tuple(sorted((v, x)))] for x in xs]
		for i in range(len(nodes)):
			M[nodes[i]].append(nodes[(i-1)%len(nodes)])
			M[nodes[i]].append(nodes[(i+1)%len(nodes)])
	return M

def dual_graph(G: dict[int, list[int]]):
	faces = [tuple(f) for f in find_faces(G)]
	nodes = [i+1 for i in range(len(faces))]
	node_to_face = dict([(i+1, f) for i,f in enumerate(faces)])
	face_to_node = dict([(f, i+1) for i,f in enumerate(faces)])

	edge_to_node = dict([(e, node) for node,face in node_to_face.items() for e in face])

	edge_to_link = dict()
	link_to_edge = dict()
	dual = dict([(i, []) for i in nodes])
	for face in faces:
		for (u, v) in face:
			dual[edge_to_node[(u,v)]].append(edge_to_node[(v,u)])
			edge_to_link[tuple(sorted((u,v)))] = tuple(sorted((edge_to_node[(u,v)], edge_to_node[(v,u)])))
			link_to_edge[tuple(sorted((edge_to_node[(u,v)], edge_to_node[(v,u)])))] = tuple(sorted((u,v)))

	return (dual, edge_to_link, link_to_edge, node_to_face, face_to_node, edge_to_node)

# When the rat-catcher is on edge e, edge f is noisy iff there is
# a closed walk of at most length k containing e* and f* in G* .
# Return the un-noisy subgraph.
def unnoisy_links_given_link(dual: dict[int, list[int]], e: tuple[int, int], k: int) -> list[tuple[int, int]]:
	s,t = e
	noisy_links = set()

	def closed_k_walks_link_set(G: dict[int, list[int]], k: int, t: int, walk_acc: list[tuple[int, int]]):
		v = walk_acc[-1][1]

		if len(walk_acc) >= k:
			return

		if v == t:
			# print(set([tuple(sorted(e)) for e in walk_acc]))
			noisy_links.update(set([tuple(sorted(e)) for e in walk_acc]))

		for u in G[v]:
			closed_k_walks_link_set(G, k, t, [*walk_acc, (v,u)])

	closed_k_walks_link_set(dual, k, t, walk_acc=[(t,s)])
	links = set([tuple(sorted((i, j))) for i in dual for j in dual[i]])
	unnoisy_links = links - noisy_links

	# print("k", k, "link", e, "noisy_links", noisy_links)
	return unnoisy_links

# When the rat-catcher is on face r, edge f is noisy iff there is
# a closed walk of at most length k containing vr* and f* in G* .
# Return the un-noisy subgraph
def unnoisy_links_given_face(dual: dict[int, list[int]], r: int, k: int) -> dict[int, list[int]]:
	noisy_links = set()

	def closed_k_walks_link_set_2(G: dict[int, list[int]], k: int, s: int, t: int, walk_acc: list[tuple[int, int]]):
		v = s

		if len(walk_acc) >= k:
			return

		if v == t:
			noisy_links.update(set([tuple(sorted(e)) for e in walk_acc]))

		for u in G[v]:
			closed_k_walks_link_set_2(G, k, t, [*walk_acc, (v,u)])

	closed_k_walks_link_set_2(dual, k, r, r, walk_acc=[])
	links = set([tuple(sorted((i, j))) for i in dual for j in dual[i]])
	unnoisy_links = links - noisy_links

	return unnoisy_links

def subgraph_given_links(G: dict[int, list[int]], links: list[tuple[int, int]], link_to_edge: dict[tuple[int,int], tuple[int, int]]) -> dict[int, list[int]]:
	unnoisy_edges = [link_to_edge[e] for e in links]
	subgraph = dict()
	for u,vs in G.items():
		for v in vs:
			if (u,v) in unnoisy_edges:
				if u not in subgraph:
					subgraph[u] = []
				subgraph[u].append(v)
				if v not in subgraph:
					subgraph[v] = []
				subgraph[v].append(u)
	for v,xs in subgraph.items():
		if len(xs) == 0:
			del subgraph[v]
	return subgraph

def flatten(xss):
	return [x for xs in xss for x in xs]

# Assume |V(G)| >= 2
# Return True if ratcatcher has a winning strategy iff
# <=> carving width < k
# <=> deg_G(v) < k for all v in V(G) and there is no antipodalities
def rat_catching_algorithm(G: dict[int, list[int]], k: int, print_escape=False) -> bool:
	for x,xs in G.items():
		if len(xs) >= k:
			return False

	edges = set([tuple(sorted((i, j))) for i in G for j in G[i]])
	faces = [tuple(f) for f in find_faces(G)]

	dual, edge_to_link, link_to_edge, node_to_face, face_to_node, edge_to_node = dual_graph(G)

	Xe = dict([(e, subgraph_given_links(G, unnoisy_links_given_link(dual, edge_to_link[e], k), link_to_edge)) for e in edges])
	Xe = dict(filter(lambda x: x[1] != {}, Xe.items()))

	Xr = dict((r, [v for v in set(G.keys()) - set(flatten(r))]) for r in faces)
	Xr = dict(filter(lambda x: len(x[1]) > 0, Xr.items()))

	at_least_one_deletion = False
	while at_least_one_deletion:
		at_least_one_deletion = False
		for r in faces:
			for e in r:
				if e in Xe and len(Xr[r]) == 0:
					del Xe[e]
					other_face = node_to_face[edge_to_node((e[1], e[0]))]
					del Xr[other_face]
					at_least_one_deletion = True
					print("A deletion was made")
		if len(Xe) == 0 or len(Xr) == 0:
			break

	if len(Xe.keys()) == 0 or len(Xr.keys()) == 0:
		# print("no escape sequence")
		return True
	else:
		if print_escape:
			print("escape sequence")
			print("Xe")
			for (e, C) in Xe.items():
				print(e, C)
			print("Xr")
			for (r, vs) in Xr.items():
				print(r, vs)
			print()
		return False

def carving_width_rat_catching(G: dict[int, list[int]]) -> int:
	l = 0
	r = 1
	while True:
		if not rat_catching_algorithm(G, r):
			l = r
			r *= 2
		else:
			break
	m = -1
	while l < r:
		m = int(math.ceil((l + r) / 2))
		if rat_catching_algorithm(G, m):
			r = m - 1
		else:
			l = m
	return l

print("cw is", carving_width_rat_catching(G))
