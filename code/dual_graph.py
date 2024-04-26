from parse_graph import parse_text_to_adj, adj_to_text

# assume planar graph
# assume not reflexive graph
# assume clockwise or counterclockwise ordering
def dual_graph(G: dict[int, list[int]]):
	G2 = dict([(x, ys.copy()) for x,ys in G.items()])

	# rotate neighbors such that parallel edges are consecutive
	def rotated(l, n):
		return l[n:] + l[:n]
	for x,ys in G2.items():
		for i,y in enumerate(ys):
			if y != ys[0]:
				G2[x] = rotated(ys, i)
				break

	# assign edge ids
	G3 = dict([(x, ys.copy()) for x,ys in G2.items()])
	def nth_to_last_idx_of(l, x, n):
		return len(l) - 1 - (l[::-1].index(x) + n)
	next_edge_id = 1
	edges = dict()
	for x,ys in G2.items():
		prev = -1
		nth = 0
		for i,y in enumerate(ys):
			if x > y: continue
			if y == prev: nth += 1
			else: nth = 0
			G3[x][i] = next_edge_id
			edges[next_edge_id] = (x, y)
			G3[y][nth_to_last_idx_of(G2[y], x, nth)] = -next_edge_id
			edges[-next_edge_id] = (y, x)
			prev = y
			next_edge_id += 1

	faces = dict()
	face_id = 1
	unvisited = set(edges.keys())
	edge_id_to_face_id = dict()
	while len(unvisited) > 0:
		init_edge_id = unvisited.pop()
		face = [init_edge_id]
		while True:
			curr_edge_id = face[-1]
			unvisited.discard(curr_edge_id)
			curr_x,curr_y = edges[curr_edge_id]
			edge_id_to_face_id[curr_edge_id] = face_id

			idx_prev = (G3[curr_y].index(-curr_edge_id)-1)%len(G3[curr_y])
			next_edge_id = G3[curr_y][idx_prev]

			if init_edge_id == next_edge_id:
				faces[face_id] = face
				face_id += 1
				break

			face.append(next_edge_id)

	dual = dict([(i, [edge_id_to_face_id[-e] for e in face]) for i,face in faces.items()])

	return dual

G = parse_text_to_adj()
dual = dual_graph(G)
adj_to_text(dual)
