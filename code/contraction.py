from parse_graph import parse_text_to_adj, adj_to_text

def contraction(G: dict[int, list[int]], e: tuple[int, int]) -> dict[int, list[int]]:
	a,b = e
	G2 = G.copy()
	
	idx1 = G2[a].index(b)
	rotated_Ga = G2[a][idx1:] + G2[a][:idx1]

	idx2 = G2[b].index(a)
	rotated_Gb = G2[b][idx2:] + G2[b][:idx2]

	c = max(G2.keys()) + 1

	G2[c] = rotated_Gb + rotated_Ga

	for x,ys in G2.items():
		G2[x] = [(c if y==a or y==b else y) for y in ys]

	del G2[b]
	del G2[a]

	G2[c] = [y for y in G2[c] if y != a and y != b and y != c]

	return G2, c

if __name__ == "__main__":
	G = parse_text_to_adj()
	input()
	G1, c = contraction(G, tuple(sorted(map(int, input().split()))))
	adj_to_text(G1)
