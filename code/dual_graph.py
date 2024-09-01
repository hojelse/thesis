from Graph import Graph, read_lmg_from_stdin

# Assume G is a rotation system
def dual_graph(G: Graph) -> tuple[Graph, dict[int, int], dict[int, int], dict[int, list[int]], dict[int, int]]:
	edges = [e for e in G.E()]

	D = Graph()
	edge_to_link: dict[int, int] = dict()
	link_to_edge: dict[int, int] = dict()
	node_to_face: dict[int, list[int]] = dict()  # nodeid to edgeid list
	edge_to_node: dict[int, int] = dict()        # half-edge to the faceid/node to its either left/right

	# Find faces
	next_nodeid = -1
	while edges:
		e = edges.pop()
		next_e = e
		edge_to_node[e] = next_nodeid
		face = [e]
		while True:
			u,v = G.edge_to_vertexpair[next_e]
			idx = G.adj_edges[v].index(-next_e)
			next_e = G.adj_edges[v][(idx-1)%len(G.adj_edges[v])]
			if (next_e == e):
				break
			edges.remove(next_e)
			face.append(next_e)
			edge_to_node[next_e] = next_nodeid
		node_to_face[next_nodeid] = face
		next_nodeid -= 1

	for i in node_to_face.keys():
		D.adj_edges[i] = []

	# Add edges to dual graph
	next_linkid = 1
	for i,f1 in node_to_face.items():
		for j,f2 in node_to_face.items():
			if i < j:
				common_edges = set(set(map(abs, f1))).intersection(set(map(abs, f2)))
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

	# todo make edge_to_link and link_to_edge redundant
	# by nameing edges and links the same

	return D, edge_to_link, link_to_edge, node_to_face, edge_to_node

if __name__ == "__main__":
	G = Graph()
	G.from_lmg(read_lmg_from_stdin())
	D, edge_to_link, link_to_edge, node_to_face, edge_to_node = dual_graph(G)
	print_adj(D.adj())
	print("edge_to_link", edge_to_link)
	print("link_to_edge", link_to_edge)
	print("node_to_face", node_to_face)
	print("edge_to_node", edge_to_node)