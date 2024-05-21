from Graph import Graph
from parse_graph import adj_to_text, parse_text_to_adj

def index_of_first(lst, pred):
	for i, v in enumerate(lst):
		if pred(v):
			return i
	return None

# assume G might have parallel edges
# assume G do not have self-loops
# assume adjacency list of G has clockwise ordering of neighbors
def contraction(G: Graph, a: int, b: int) -> Graph:
	# copy G
	G1 = G.copy()

	# create new vertex c
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

	# remove self-loops on c
	G1.adj_edges[c] = [e for e in G1.adj_edges[c] if not (G1.edge_to_vertexpair[e][0] == G1.edge_to_vertexpair[e][1] == c)]
	G1.edge_to_vertexpair = dict([(k,v) for k,v in G1.edge_to_vertexpair.items() if not (v[0] == v[1] == c)])

	# remove a and b
	del G1.adj_edges[a]
	del G1.adj_edges[b]

	return G1, c

if __name__ == "__main__":
	a,b = map(int, input().split())
	adj = parse_text_to_adj()

	G = Graph()
	G.from_adj(adj)
	G1, c = contraction(G, a, b)
	adj_to_text(G1.adj())
	print("c", c)
