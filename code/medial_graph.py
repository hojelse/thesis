from Graph import Graph, read_lmg_from_stdin

# assume G is simple
# assume G is planar
# assume G_adj is a rotation system
# guarantee an edge of G have the same id as its corresponding medial node
# guarantee M is a rotation system
def medial_graph(G: Graph):
	M = Graph()
	M.adj_edges = dict((abs(n), []) for n in G.edge_to_vertexpair.keys())

	# Find faces
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

	# Add edges to medial graph
	next_linkid = 1
	for face in faces:
		for i in range(len(face)):
			n1 = abs(face[i])
			n2 = abs(face[(i+1)%len(face)])
			M.adj_edges[n1].append(next_linkid)
			M.adj_edges[n2].append(-next_linkid)
			M.edge_to_vertexpair[next_linkid] = (n1, n2)
			M.edge_to_vertexpair[-next_linkid] = (n2, n1)
			next_linkid += 1
		n1 = abs(face[0])
		e1 = M.adj_edges[n1].pop()
		e2 = M.adj_edges[n1].pop()
		M.adj_edges[n1].append(e1)
		M.adj_edges[n1].append(e2)

	# Make clockwise ordering of neighbors
	for v,es in M.adj_edges.items():
		M.adj_edges[v] = list(reversed(es))

	return M, dict([(k,v) for k,v in G.edge_to_vertexpair.items() if k > 0])

if __name__ == "__main__":
	G = Graph()
	G.from_lmg(read_lmg_from_stdin())
	print(medial_graph(G))
