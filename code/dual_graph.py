from parse_graph import parse_text_to_adj, adj_to_text

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

def dual_graph(G: dict[int, list[int]]):
	faces = [tuple(f) for f in find_faces(G)]
	nodes = [i+1 for i in range(len(faces))]
	node_to_face = dict([(i+1, f) for i,f in enumerate(faces)])
	face_to_node = dict([(f, i+1) for i,f in enumerate(faces)])

	edge_to_node = dict([(e, node) for node,face in node_to_face.items() for e in face])

	edge_to_link = dict()
	link_to_edges = dict()
	dual = dict([(i, []) for i in nodes])
	for face in faces:
		for (u, v) in face:
			dual[edge_to_node[(u,v)]].append(edge_to_node[(v,u)])
			edge_to_link[tuple(sorted((u,v)))] = tuple(sorted((edge_to_node[(u,v)], edge_to_node[(v,u)])))

			link = tuple(sorted((edge_to_node[(u,v)], edge_to_node[(v,u)])))
			edge = tuple(sorted((u,v)))
			if link in link_to_edges:
				link_to_edges[link].append(edge)
			else:
				link_to_edges[link] = [edge]

	return dual, edge_to_link, link_to_edges, node_to_face, face_to_node, edge_to_node

# G = parse_text_to_adj()
# dual, edge_to_link, link_to_edges, node_to_face, face_to_node, edge_to_node = dual_graph(G)
# adj_to_text(dual)