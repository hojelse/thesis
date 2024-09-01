from util import adj_from_stdin

G = adj_from_stdin()

def is_undirected(G):
	for x,ys in G.items():
		for y in ys:
			if x not in G[y]:
				return False
	return True

print(is_undirected(G))
