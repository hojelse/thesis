from parse_graph import parse_graph_to_adj, adj_to_bytes

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

def closed_k_walks_link_set(G: dict[int, list[int]], k: int, t: int, walk_acc: list[tuple[int, int]], depth: int) -> set[tuple[int, int]]:
	v = walk_acc[-1][1]
	if v == t and len(walk_acc) == k:
		return set([tuple(sorted(e)) for e in walk_acc])
	elif len(walk_acc) >= k:
		return set()

	link_set = set()
	for u in G[v]:
		link_set.update(closed_k_walks_link_set(G, k, t, [*walk_acc, (v,u)], depth+1))
	
	return link_set

def closed_k_walks_link_set_2(G: dict[int, list[int]], k: int, s: int, t: int, walk_acc: list[tuple[int, int]], depth: int) -> set[tuple[int, int]]:
	v = s
	if v == t and len(walk_acc) == k:
		return set([tuple(sorted(e)) for e in walk_acc])
	elif len(walk_acc) >= k:
		return set()

	link_set = set()
	for u in G[v]:
		link_set.update(closed_k_walks_link_set(G, k, t, [*walk_acc, (v,u)], depth+1))
	
	return link_set

# When the rat-catcher is on edge e, edge f is noisy iff there is
# a closed walk of at most length k containing e* and f* in G* .
# Return the un-noisy subgraph.
def unnoisy_links_given_link(dual: dict[int, list[int]], e: tuple[int, int], k: int) -> list[tuple[int, int]]:
	s,t = e

	noisy_links = closed_k_walks_link_set(dual, k, t, walk_acc=[(t,s)], depth=1)
	links = set([tuple(sorted((i, j))) for i in dual for j in dual[i]])
	unnoisy_links = links - noisy_links

	return unnoisy_links

# When the rat-catcher is on face r, edge f is noisy iff there is
# a closed walk of at most length k containing vr* and f* in G* .
# Return the un-noisy subgraph
def unnoisy_links_given_face(dual: dict[int, list[int]], r: int, k: int) -> dict[int, list[int]]:

	noisy_links = closed_k_walks_link_set_2(dual, k, r, r, walk_acc=[], depth=1)
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

# Return True if carving width is at least k
def rat_catching_algorithm(G: dict[int, list[int]], k: int) -> bool:
	edges = set([tuple(sorted((i, j))) for i in G for j in G[i]])
	faces = [tuple(f) for f in find_faces(G)]

	dual, edge_to_link, link_to_edge, node_to_face, face_to_node, edge_to_node = dual_graph(G)

	Xe = dict([(e, subgraph_given_links(G, unnoisy_links_given_link(dual, edge_to_link[e], k), link_to_edge)) for e in edges])
	Xr = dict((r, [v for v in set(G.keys()) - set(flatten(r))]) for r in faces)

	Xe = dict(filter(lambda x: x[1] != {}, Xe.items()))

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

	if len(Xe) == 0 or len(Xr) == 0:
		# print("no escape sequence")
		return False
	else:
		# print("Xe")
		# for (e, C) in Xe.items():
		# 	print(e, C)
		# print("Xr")
		# for (r,vs) in Xr.items():
		# 	for v in vs:
		# 		print(r, v)
		# print()
		return True

def carving_width(G: dict[int, list[int]]) -> int:
	k_l = 0
	k_r = 1
	while True:
		if rat_catching_algorithm(G, k_r):
			k_l = k_r
			k_r *= 2
		else:
			break

	k = -1
	while k_l < k_r:
		k = (k_l + k_r) // 2
		if rat_catching_algorithm(G, k):
			k_l = k + 1
		else:
			k_r = k
	return k

### Brute force

def brute_force_carving_width(G: dict[int, list[int]]) -> bool: # with dp
	return min(carving_decomposition_width(G, cd) for cd in carving_decompositions(G))

def carving_decomposition_width(G: dict[int, list[int]], cd) -> int:
	root,t = cd
	width = 0
	for x, ys in t.items():
		for y in ys:
			width = max(width, partition_width(G, t, x, y))
	return width

def partition_width(G, t, x, y) -> int:
	root_x = x
	while True:
		stop = True
		for v in t[root_x]:
			if y == v:
				continue
			if len(v) > len(root_x):
				root_x = v
				stop = False
		if stop:
			break
	root_y = y
	while True:
		stop = True
		for v in t[root_y]:
			if x == v:
				continue
			if len(v) > len(root_y):
				root_y = v
				stop = False
		if stop:
			break

	smaller, vertex_set = (root_x, root_y) if len(root_x) < len(root_y) else (root_y, root_x)
	part1 = set(vertex_set) - set(smaller)
	part2 = set(smaller)

	count = 0

	for root_x in part1:
		for root_y in part2:
			if root_x in G[root_y]:
				count += 1
	return count

def carving_decompositions(G: dict[int, list[int]]):
	x = tuple(sorted(G.keys()))

	if len(x) == 2:
		x0 = tuple([x[0]])
		x1 = tuple([x[1]])
		return [(x0, {x0: [x1], x1: [x0]})]

	carvings = []
	for i in range(1, len(x)):
		for j in range(i+1, len(x)):
			l1 = x[:i]
			m1 = x[i:j]
			r1 = x[j:]
			for root_l, ts_l in carving_binary(l1):
				for root_m, ts_m in carving_binary(m1):
					for root_r, ts_r in carving_binary(r1):
						t = {
							x: [root_l, root_m, root_r],
							**ts_l,
							**ts_m,
							**ts_r,
						}
						t[root_l].append(x)
						t[root_m].append(x)
						t[root_r].append(x)
						carvings.append((x, t))
	return carvings

def carving_binary(x: tuple[int]):
	x = tuple(sorted(x))
	if len(x) == 1:
		return [(x, {x: []})]
	
	ts = []
	for i in range(1, len(x)):
		l = x[:i]
		r = x[i:]
		for root_l, ts_l in carving_binary(l):
			for root_r, ts_r in carving_binary(r):
				t = {
					x: [root_l, root_r],
					**ts_l,
					**ts_r,
				}
				t[root_l].append(x)
				t[root_r].append(x)
				ts.append((x, t))

	return ts

print("cw is", carving_width(G))
print("cw brute", brute_force_carving_width(G))