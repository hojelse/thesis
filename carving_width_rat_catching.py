from parse_graph import parse_graph_to_adj, adj_to_bytes
from dual_graph import dual_graph, find_faces
import math

def carving_width_rat_catching(G) -> int:
	dual, edge_to_link, link_to_edges, node_to_face, face_to_node, edge_to_node = dual_graph(G)
	# When the rat-catcher is on edge e, edge f is noisy iff there is
	# a closed walk of at most length k containing e* and f* in G* .
	# Return the un-noisy subgraph.
	def noisy_links(l: tuple[int, int], k: int) -> set[tuple[int, int]]:
		s,t = l
		noisy = set()
		def bfs(walk_acc: list[tuple[int, int]]):
			if len(walk_acc) == k: return
			v = walk_acc[-1][1]
			if v == t:
				noisy.update([tuple(sorted(e)) for e in walk_acc])
			for u in dual[v]:
				bfs(walk_acc + [(v, u)])
		bfs([(t, s)])
		return noisy

	def quiet_links(l: tuple[int, int], k: int) -> set[tuple[int, int]]:
		links = [tuple(sorted((x,y))) for (x,ys) in dual.items() for y in ys]
		return set(links) - noisy_links(l, k)

	def quiet_edges(e: tuple[int, int], k: int) -> set[tuple[int, int]]:
		quiet = set()
		l = edge_to_link[tuple(sorted(e))]
		for link in quiet_links(l, k):
			for edge in link_to_edges[link]:
				quiet.add(tuple(sorted(edge)))
		return quiet

	def quiet_components(e: tuple[int, int], k: int) -> dict[int, list[int]]:
		edges = quiet_edges(e, k)

		quiet_subgraph = {v: [] for v in G.keys()}
		for (u, v) in edges:
			quiet_subgraph[u].append(v)
			quiet_subgraph[v].append(u)

		components = []
		unseen = set(quiet_subgraph.keys())

		while len(unseen) > 0:
			v = unseen.pop()
			component = [v]
			stack = [v]
			while len(stack) > 0:
				v = stack.pop()
				for u in quiet_subgraph[v]:
					if u in unseen:
						unseen.remove(u)
						stack.append(u)
						component.append(u)
			components.append(component)

		return components

	def flatten(xss):
		return set([x for xs in xss for x in xs])

	# Assume |V(G)| >= 2
	# Return True
	# iff. carving-width >= k
	# iff. rat has a winning escape strategy with noise-level k
	def rat_wins(k: int) -> bool:
		if len(G) < 2:
			return False
		
		if max([len(G[v]) for v in G]) >= k:
			return True

		# print("k is", k)
		edge_set = set([tuple(sorted((i, j))) for i in G for j in G[i]])

		Te = set([(e, tuple(C)) for e in edge_set for C in quiet_components(e, k)])
		Sr = set([(r, v) for r in node_to_face.keys() for v in G.keys()])

		# print("Sr")
		# for (r, v) in sorted(Sr):
		# 	print(r, ":", v)
		# print("Te")
		# for (e, C) in sorted(Te):
		# 	print(e, ":", sorted(C))

		losing_eC = set()
		losing_rv = set()

		for (r, v) in Sr:
			if v in flatten(node_to_face[r]):
				losing_rv.add((r,v))

		if len(Te) == len(losing_eC) or len(Sr) == len(losing_rv):
			return False

		while True:
			new_deletion = False

			for (e, C) in Te:
				if all([(edge_to_node[e], v) in losing_rv for v in C]):
					if (e, C) not in losing_eC:
						new_deletion = True
						losing_eC.add((e, C))
			
			for (e, C) in losing_eC:
				r1 = edge_to_node[e]
				r2 = edge_to_node[e[::-1]]
				for (r, v) in [(r1, v) for v in C] + [(r2, v) for v in C]:
					if (r, v) not in losing_rv:
						new_deletion = True
						losing_rv.add((r, v))

			if len(Te) == len(losing_eC) or len(Sr) == len(losing_rv):
				return False
			elif not new_deletion:
				return True
			
	def binary_search_cw():
		l = 0
		r = 1
		while True:
			if rat_wins(r):
				l = r
				r *= 2
			else:
				break
		m = l
		while l < r:
			m = int(math.ceil((l + r) / 2))
			if rat_wins(m):
				l = m
			else:
				r = m - 1
		return l
	
	return binary_search_cw()

G = parse_graph_to_adj()
cw = carving_width_rat_catching(G)
print("cw is", cw)

