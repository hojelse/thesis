import itertools
from parse_graph import parse_text_to_adj

G: dict[int, list[int]] = parse_text_to_adj()
vertex_set = G.keys()
N = len(vertex_set)

def valid(cycle: list[int]) -> bool:
	for i in range(0, N-1):
		if not cycle[i+1] in G[cycle[i]]:
			return False
	if not cycle[0] in G[cycle[-1]]:
		return False
	return True

def count_ham_cyc() -> int:
	cycles = itertools.permutations(vertex_set)
	count = 0
	for cycle in cycles:
		if valid(cycle):
			count += 1
	return count//(2*N)

print(count_ham_cyc())
