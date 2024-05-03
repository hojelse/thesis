from parse_graph import parse_text_to_adj, adj_to_text
# Assume planar and clockwise ordering
def medial_graph(G: dict[int, list[int]]):
	es = set([tuple(sorted((i, j))) for i in G for j in G[i]])

	edge_to_node = dict([(e, i+1) for i,e in enumerate(es)])
	node_to_edge = dict([(i+1, e) for i,e in enumerate(es)])

	medial = dict([(i+1, []) for i in range(len(es))])

	for v,xs in G.items():
		nodes = [edge_to_node[tuple(sorted((v, x)))] for x in xs]
		for i in range(len(nodes)):
			medial[nodes[i]].append(nodes[(i-1)%len(nodes)])
			medial[nodes[i]].append(nodes[(i+1)%len(nodes)])
	return medial, node_to_edge, edge_to_node

if __name__ == "__main__":
	G = parse_text_to_adj()
	medial, node_to_edge, edge_to_node = medial_graph(G)
	adj_to_text(medial)
	print(len(edge_to_node))
	for e,x in edge_to_node.items():
		print(e[0], e[1], x)