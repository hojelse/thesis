from parse_graph import parse_text_to_adj, adj_to_text
adj = parse_text_to_adj()

vertices = list(adj.keys())
rotated = vertices[1:] + vertices[:1]

mapping = dict([(vertices[i], rotated[i]) for i in range(len(vertices))])

P = dict([(v, []) for v in vertices])

for i in adj:
	for j in adj[i]:
		P[mapping[i]].append(mapping[j])

adj_to_text(P)