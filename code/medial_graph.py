import log
from Graph import Graph
from parse_graph import adj_to_text, adj_to_text_2, parse_text_to_adj

# assume G is simple
# assume G is planar
# assume G_adj is a rotation system
# guarantee M is a rotation system
def medial_graph(G_adj: dict[int, list[int]]) -> Graph:
	vertexpairs = set([tuple(sorted((i, j))) for i in G_adj for j in G_adj[i]])

	vertexpair_to_node = dict([(e, i+1) for i,e in enumerate(vertexpairs)])
	node_to_vertexpair = dict([(i+1, e) for i,e in enumerate(vertexpairs)])

	medial = dict([(i+1, []) for i in range(len(vertexpairs))])

	for u,vs in G_adj.items():
		nodes = [vertexpair_to_node[tuple(sorted((u, v)))] for v in vs]
		for i in range(len(nodes)):
			medial[nodes[i]].append(nodes[(i-1)%len(nodes)])
			medial[nodes[i]].append(nodes[(i+1)%len(nodes)])

	M = Graph()
	M.from_adj(medial)
	# log.add("Medial graph: " + str(M))
	# log.add("Node to vertexpair: " + str(node_to_vertexpair))
	return M, node_to_vertexpair

# assume G is simple
# assume G is planar
# assume G_adj is a rotation system
# guarantee an edge of G have the same id as its corresponding medial node
# guarantee M is a rotation system
def medial_graph_2(G_adj: dict[int, list[int]]):
	G = Graph()
	G.from_adj(G_adj)

	M = Graph()
	M.adj_edges = dict((abs(n), []) for n in G.edge_to_vertexpair.keys())

	# print(M.adj_edges)

	edges = [e for e in G.E()]
	faces = []
	while len(edges) > 0:
		e = edges.pop()
		next_e = e
		face = [e]
		while True:
			u,v = G.edge_to_vertexpair[next_e]
			idx = G.adj_edges[v].index(-next_e)
			next_e = G.adj_edges[v][(idx-1)%len(G.adj_edges[v])]
			if (next_e == e):
				break
			edges.remove(next_e)
			face.append(next_e)
		faces.append(face)

	next_linkid = 1
	for face in faces:
		for i in range(len(face)):
			n1 = abs(face[i])
			n2 = abs(face[(i-1)%len(face)])
			M.adj_edges[n1].append(next_linkid)
			M.adj_edges[n2].append(-next_linkid)
			M.edge_to_vertexpair[next_linkid] = (n1, n2)
			M.edge_to_vertexpair[-next_linkid] = (n2, n1)
			next_linkid += 1

	for v,es in M.adj_edges.items():
		M.adj_edges[v] = [es[2], es[3], es[1], es[0]]

	# log.add("Medial graph: " + str(M))
	return M, dict([(k,v) for k,v in G.edge_to_vertexpair.items() if k > 0])

if __name__ == "__main__":
	adj = parse_text_to_adj()
	G = Graph()
	G.from_adj(adj)
	print(G)

	# M, node_to_vertexpair = medial_graph(adj)
	# adj_to_text(M.adj())
	# print("node_to_vertexpair", node_to_vertexpair)

	# M, node_to_vertexpair = medial_graph(adj)
	# print(M)
	# print("node_to_vertexpair", node_to_vertexpair)
