from parse_graph import parse_text_to_adj, adj_to_text

# assume planar graph
# assume not reflexive graph
# assume clockwise or counterclockwise ordering
def dual_graph(G: dict[int, list[int]]):

	# rotate neighbors such that parallel edges are consecutive
	G2 = dict([(x, ys.copy()) for x,ys in G.items()])

	def rotated(l: list[int], n: int):
		return l[n:] + l[:n]

	for x,ys in G2.items():
		for i,y in enumerate(ys):
			if y != ys[0]:
				G2[x] = rotated(ys, i)
				break

	# assign edge ids
	# where the pair of ids, i and -i, are the two directions of the same edge
	# and ordering is maintained
	_G = dict([(x, ys.copy()) for x,ys in G2.items()])
	edgeid_to_vertexpair = dict()

	def opposite_idx(neighbors: list[int], nth_parallel: int, v: int):
		return len(neighbors) - 1 - (neighbors[::-1].index(v) + nth_parallel)

	next_edgeid = 1
	for x,ys in G2.items():
		prev = 0
		nth_parallel = 0
		for i,y in enumerate(ys):
			if x > y: continue
			if y == prev: nth_parallel += 1
			else: nth_parallel = 0
			_G[x][i] = next_edgeid
			edgeid_to_vertexpair[next_edgeid] = (x, y)
			_G[y][opposite_idx(G2[y], nth_parallel, x)] = -next_edgeid
			edgeid_to_vertexpair[-next_edgeid] = (y, x)
			prev = y
			next_edgeid += 1

	# construct dual graph
	nodeid_to_edgeids = dict()
	edgeids_to_nodeid = dict()

	edgeid_to_nodeid = dict()

	next_nodeid = 1
	unvisited = set(edgeid_to_vertexpair.keys())
	while len(unvisited) > 0:
		init_edge_id = unvisited.pop()
		edgeids = [init_edge_id]
		while True:
			curr_edgeid = edgeids[-1]
			unvisited.discard(curr_edgeid)
			curr_x,curr_y = edgeid_to_vertexpair[curr_edgeid]
			edgeid_to_nodeid[curr_edgeid] = next_nodeid

			idx_prev = (_G[curr_y].index(-curr_edgeid)-1)%len(_G[curr_y])
			next_edgeid = _G[curr_y][idx_prev]

			if init_edge_id == next_edgeid:
				nodeid_to_edgeids[next_nodeid] = edgeids
				edgeids_to_nodeid[frozenset(edgeids)] = next_nodeid
				next_nodeid += 1
				break

			edgeids.append(next_edgeid)

	_D = dict([(i, []) for i in nodeid_to_edgeids.keys()])
	linkid_to_nodepair = dict()
	edgeid_to_linkid = dict()
	linkid_to_edgeid = dict()
	next_linkid = 1

	for e1,n1 in edgeid_to_nodeid.items():
		if e1 < 0: continue
		e2 = -e1
		n2 = edgeid_to_nodeid[e2]
		linkid_to_nodepair[next_linkid] = (n1, n2)
		linkid_to_nodepair[-next_linkid] = (n2, n1)
		edgeid_to_linkid[e1] = next_linkid
		linkid_to_edgeid[next_linkid] = e1
		edgeid_to_linkid[e2] = -next_linkid
		linkid_to_edgeid[-next_linkid] = e2
		_D[n1].append(next_linkid)
		_D[n2].append(-next_linkid)
		next_linkid += 1

	D = dict([(i, list(map(lambda x: linkid_to_nodepair[x][1], linkids))) for i,linkids in _D.items()])

	return D, _D, linkid_to_nodepair, edgeid_to_linkid, linkid_to_edgeid, nodeid_to_edgeids, edgeid_to_nodeid, edgeid_to_vertexpair, _G, G

# G = parse_text_to_adj()
# D, _D, linkid_to_nodepair, edgeid_to_linkid, linkid_to_edgeid, nodeid_to_edgeids, edgeid_to_nodeid, G, _G, edgeid_to_vertexpair = dual_graph(G)
# adj_to_text(D)

# print("G", G)
# print("_G", _G)
# print("edgeid_to_vertexpair", edgeid_to_vertexpair)
# print("D", D)
# print("_D", _D)
# print("linkid_to_nodepair", linkid_to_nodepair)
# print("nodeid_to_edgeids", nodeid_to_edgeids)
# print("edgeid_to_nodeid", edgeid_to_nodeid)
# print("edgeid_to_linkid", edgeid_to_linkid)
# print("linkid_to_edgeid", linkid_to_edgeid)
