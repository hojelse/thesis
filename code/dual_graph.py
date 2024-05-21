from Graph import Graph
from parse_graph import adj_to_text, parse_text_to_adj

def dual_graph(G: Graph) -> Graph:
	edges = [e for e in G.E()]

	D = Graph()
	edge_to_link = dict()
	link_to_edge = dict()
	node_to_face = dict()
	edge_to_node = dict()

	next_nodeid = -1
	while edges:
		e = edges.pop()
		next_e = e
		edge_to_node[e] = next_nodeid
		face = [e]
		while True:
			u,v = G.edge_to_vertexpair[next_e]
			idx = G.adj_edges[v].index(-next_e)
			next_e = G.adj_edges[v][(idx-1)%len(G.adj_edges[v])]
			if (next_e == e):
				break
			edges.remove(next_e)
			face.append(next_e)
			edge_to_node[next_e] = next_nodeid
		node_to_face[next_nodeid] = face
		next_nodeid -= 1

	for i in node_to_face.keys():
		D.adj_edges[i] = []

	next_linkid = 1
	for i,f1 in node_to_face.items():
		for j,f2 in node_to_face.items():
			if i < j:
				common_edges = set(list(map(abs, f1))).intersection(set(map(abs, f2)))
				for e in common_edges:
					D.edge_to_vertexpair[next_linkid] = (i, j)
					D.edge_to_vertexpair[-next_linkid] = (j, i)
					edge_to_link[e] = next_linkid
					link_to_edge[next_linkid] = e
					edge_to_link[-e] = -next_linkid
					link_to_edge[-next_linkid] = -e
					D.adj_edges[i].append(next_linkid)
					D.adj_edges[j].append(-next_linkid)
					next_linkid += 1

	return D, edge_to_link, link_to_edge, node_to_face, edge_to_node

if __name__ == "__main__":
	adj = parse_text_to_adj()
	G = Graph()
	G.from_adj(adj)
	D, edge_to_link, link_to_edge, node_to_face, edge_to_node = dual_graph(G)
	adj_to_text(D.adj())
	print("edge_to_link", edge_to_link)
	print("link_to_edge", link_to_edge)
	print("node_to_face", node_to_face)
	print("edge_to_node", edge_to_node)