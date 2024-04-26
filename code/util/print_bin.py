from parse_graph import adj_to_bytes
adj = {
	1: [2,3,4,5,6],
	2: [3,1,6],
	3: [4,1,2],
	4: [5,1,3],
	5: [6,1,4],
	6: [2,1,5],
}

adj_to_bytes(adj)
