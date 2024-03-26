from parse_graph import parse_graph_to_adj
from itertools import combinations

G = parse_graph_to_adj()
vertex_set = set(G.keys())

# carving width = minimum carving decomposition width
def carving_width(G: dict[int, list[int]]):
	return min([decomposition_width(d) for d in decompositions_partitions(vertex_set)])

# decomposition width = maximum partition width
def decomposition_width(d):
	return max([partition_width(G, part) for part in d])

def decompositions_partitions(xs: set[int]) -> list[list[tuple[set[int], set[int]]]]:
	if len(xs) == 1:
		return [[(set(xs), vertex_set-set(xs))]]
	parts = []
	for (A, B) in partitions(xs):
		for dA in decompositions_partitions(A):
			for dB in decompositions_partitions(B):
				parts.append([(A, vertex_set-A), (B, vertex_set-B), *dA, *dB])
	return parts

def decompositions(xs: set[int]):
	if len(xs) == 1:
		return list(xs)
	decomps = []
	for (A, B) in partitions(xs):
		for dA in decompositions(A):
			for dB in decompositions(B):
				decomps.append([dA, dB])
	return decomps

# partition width = number of edges in G crossing the partition
partition_width_cache = dict()
def partition_width(G, partition: tuple[set[int], set[int]]):
	(A, B) = partition
	t_AB = (tuple(A), tuple(B))
	t_BA = (tuple(B), tuple(A))

	if (t_AB) in partition_width_cache: return partition_width_cache[t_AB]
	if (t_BA) in partition_width_cache: return partition_width_cache[t_BA]

	w = len([(u, v) for u in A for v in B if v in G[u]])

	partition_width_cache[t_AB] = w
	partition_width_cache[t_BA] = w

	return w

def partitions(s):
	s = list(s)
	x = len(s)
	for i in range(1, (1<<x)//2):
		A = set([s[j] for j in range(x) if (i & (1 << j))])
		B = set(s) - A
		yield (A, B)

print(carving_width(G))
