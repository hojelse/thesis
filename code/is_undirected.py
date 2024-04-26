from parse_graph import parse_text_to_adj

G = parse_text_to_adj()

def is_undirected(G):
	for x,ys in G.items():
		for y in ys:
			if x not in G[y]:
				return False
	return True

print(is_undirected(G))
