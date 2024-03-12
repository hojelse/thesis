from parse_graph import parse_graph_to_adj

G = parse_graph_to_adj()

def find_faces(adj: dict[int, list[int]]) -> list[list[(int, int)]]:
	# assume planar graph
	# assume clockwise or counterclockwise ordering
	edges = set([(i, j) for i in adj for j in adj[i]])
	faces = []
	while len(edges) > 0:
		first_edge = edges.pop()
		v = first_edge[1]
		face = [first_edge]
		next_edge = first_edge
		while True:
			u = adj[next_edge[1]][(adj[next_edge[1]].index(next_edge[0])+1)%3]
			next_edge = (v, u)
			if next_edge == first_edge:
				faces.append(face)
				break
			edges.remove(next_edge)
			face.append(next_edge)
			v = u
	return faces

# Assume planar cubic with clockwise ordering
def medial_graph(G):
	fs = find_faces(G)
	es = set([tuple(sorted((i, j))) for i in G for j in G[i]])

	edge_to_node = dict([(e, i+1) for i,e in enumerate(es)])
	node_to_edge = dict([(i+1, e) for i,e in enumerate(es)])

	M = dict([(i+1, []) for i in range(len(es))])

	for v,xs in G.items():
		node1 = edge_to_node[tuple(sorted((v, xs[0])))]
		node2 = edge_to_node[tuple(sorted((v, xs[1])))]
		node3 = edge_to_node[tuple(sorted((v, xs[2])))]
		M[node1].extend([node2, node3])
		M[node2].extend([node3, node1])
		M[node3].extend([node1, node2])

	return M

def rat_catching_alg():
	pass

def edge_contraction_alg():
	pass

def opt_carving_decomp():
	pass

def opt_branch_decomp():
	M = medial_graph(G)
	Gc = opt_carving_decomp(M)

	# translate the carving decomposition into a branch decomposition
	Gb = Gc
	pass


medial_graph(G)