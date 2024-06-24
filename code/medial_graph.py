from Graph import Graph
from parse_graph import adj_to_text, parse_text_to_adj

# assume planar graph
# assume G_adj is a rotation system
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
	return M, node_to_vertexpair, vertexpair_to_node

if __name__ == "__main__":
	adj = parse_text_to_adj()
	M, node_to_vertexpair, vertexpair_to_node = medial_graph(adj)
	adj_to_text(M.adj())
	print("node_to_vertexpair", node_to_vertexpair)
	print("vertexpair_to_node", vertexpair_to_node)
