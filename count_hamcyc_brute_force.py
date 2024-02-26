import networkx as nx
import itertools
from parse_graph import parse_graph

G = parse_graph()

N = len(G.nodes)
vertex_set = list(G.nodes)

def cycle_exists(cycle):
	for i in range(len(cycle)-1):
		if cycle[i] in G[cycle[i+1]]:
			pass
		else:
			return False
	if not cycle[0] in G[cycle[-1]]:
		return False
	return True

def count_ham_cyc():
	ham_cycles = []
	cycles = list(itertools.permutations(vertex_set))
	finger_prints = set()
	count = 0
	for cycle in cycles:
		if cycle_exists(cycle):
			count += 1

			finger_print = str(sorted(map(sorted, zip(cycle, list(cycle[1:]) + [cycle[0]]))))
			if not finger_print in finger_prints:
				ham_cycles.append(cycle)
			finger_prints.add(finger_print)

	print(f"{count//N//2}")
	print(f"count: {count}")
	print(f"unique: {count//N//2}")
	for ham_cyc in ham_cycles:
		print(ham_cyc)

count_ham_cyc()

