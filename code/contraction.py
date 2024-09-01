from Graph import Graph, read_lmg_from_stdin

# assume G might have parallel edges and self-loops
# assume adjacency list of G has clockwise ordering of neighbors
# assume a != b
def contraction(G: Graph, a: int, b: int) -> tuple[Graph, int]:
	# copy G
	G1 = G.copy()

	# create new vertex c
	c = max(G1.adj_edges.keys()) + 1

	# find edges connecting a and b
	edges_a_b = []
	for e in G1.adj_edges[a] + G1.adj_edges[b]:
		u,v = G1.edge_to_vertexpair[e]
		if (u == a and v == b) or (u == b and v == a):
			edges_a_b.append(e)

	# create neighborhood of c while preserving clockwise ordering
	idx1 = G1.adj_edges[a].index(edges_a_b[0])
	rotated_Ga = G1.adj_edges[a][idx1:] + G1.adj_edges[a][:idx1]

	idx2 = G1.adj_edges[b].index(-edges_a_b[0])
	rotated_Gb = G1.adj_edges[b][idx2:] + G1.adj_edges[b][:idx2]

	G1.adj_edges[c] = rotated_Ga + rotated_Gb

	# let every edge incident to a or b be incident to c instead
	for e in G1.E():
		u,v = G1.edge_to_vertexpair[e]
		if u == a or u == b:
			G1.edge_to_vertexpair[e] = (c, v)
		u,v = G1.edge_to_vertexpair[e]
		if v == a or v == b:
			G1.edge_to_vertexpair[e] = (u, c)

	# remove all edges connecting a and b
	G1.adj_edges[c] = [e for e in G1.adj_edges[c] if e not in edges_a_b]
	G1.edge_to_vertexpair = dict([(e,uv) for e,uv in G1.edge_to_vertexpair.items() if e not in edges_a_b])

	# remove a and b
	del G1.adj_edges[a]
	del G1.adj_edges[b]

	return G1, c

if __name__ == "__main__":
	a,b = map(int, input().split())
	G = Graph()
	G.from_lmg(read_lmg_from_stdin())
	G1, c = contraction(G, a, b)
	print(G1)
	print("c", c)
