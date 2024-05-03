from parse_graph import parse_text_to_adj, adj_to_text

def contraction(G: dict[int, list[int]], e: tuple[int, int]) -> dict[int, list[int]]:
	a,b = e

	idx1 = G[a].index(b)
	rotated_Ga = G[a][idx1:] + G[a][:idx1]

	idx2 = G[b].index(a)
	rotated_Gb = G[b][idx2:] + G[b][:idx2]

	c = max(G.keys()) + 1

	G[c] = rotated_Gb + rotated_Ga

	for x,ys in G.items():
		G[x] = [(c if y==a or y==b else y) for y in ys]

	del G[b]
	del G[a]

	G[c] = [y for y in G[c] if y != a and y != b and y != c]

	return G, c

if __name__ == "__main__":
	G = parse_text_to_adj()
	input()
	G1, c = contraction(G, tuple(sorted(map(int, input().split()))))
	adj_to_text(G1)
