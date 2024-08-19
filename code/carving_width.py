import math

from Graph import Graph
from parse_graph import adj_to_text, adj_to_text_2, parse_text_to_adj
from dual_graph import dual_graph

def carving_width(G: Graph) -> int:
	D, edge_to_link, link_to_edge, node_to_face, edge_to_node = dual_graph(G)

	# If the rat-catcher is on edge e1, then edge e2 is noisy iff there is
	# a closed walk of length scrictly less than k containing e1* and e2* in the dual G*.

	def noisy_links(l: int, k: int) -> set[int]:
		s,t = D.edge_to_vertexpair[l]
		links = link_to_edge.keys()

		def dists(n: int) -> dict[int, int]:
			dist = {v: -1 for v in D.V()}
			dist[n] = 0
			queue = [n]
			while len(queue) > 0:
				v = queue.pop(0)
				for y in D.N(v):
					if dist[y] == -1:
						dist[y] = dist[v] + 1
						queue.append(y)
			return dist
		
		dist_s = dists(s)
		dist_t = dists(t)

		noisy = []
		for l1 in links:
			u,v = D.edge_to_vertexpair[l1]
			if min(
				dist_s[u] + dist_t[v] + 2,
				dist_s[v] + dist_t[u] + 2
			) < k:
				noisy.append(l1)

		return set([abs(e) for e in noisy])

	def quiet_links(l: int, k: int) -> set[int]:
		links = set([abs(e) for e in D.E()])
		return links - noisy_links(l, k)

	def quiet_edges(e: int, k: int) -> set[int]:
		return set([abs(link_to_edge[l]) for l in quiet_links(edge_to_link[e], k)])

	def quiet_components(e: int, k: int) -> list[list[int]]:
		edges = quiet_edges(e, k)

		quiet_subgraph = {v: [] for v in G.V()}
		for e1 in edges:
			u,v = G.edge_to_vertexpair[e1]
			quiet_subgraph[u].append(e1)
			quiet_subgraph[v].append(-e1)

		components = []
		unseen = set(quiet_subgraph.keys())

		while len(unseen) > 0:
			v = unseen.pop()
			component = [v]
			stack = [v]
			while len(stack) > 0:
				v = stack.pop()
				for e1 in quiet_subgraph[v]:
					u,v = G.edge_to_vertexpair[e1]
					if v in unseen:
						unseen.remove(v)
						stack.append(v)
						component.append(v)
			components.append(component)

		return components

	def flatten(xss):
		return set([x for xs in xss for x in xs])

	# Assume |V(G)| >= 2
	# Return True
	# iff. carving-width >= k
	# iff. rat has a winning escape strategy with noise-level k
	def rat_wins(k: int) -> bool:
		if len(G.V()) < 2:
			return False
		
		if max([len(G.N(v)) for v in G.V()]) >= k:
			return True

		# Set up the game states
		halfedges = edge_to_link.keys()

		T = set([(e, tuple(C)) for e in halfedges for C in quiet_components(e, k)])
		S = set([(f, v) for f in node_to_face.keys() for v in G.V()])

		# Set up the losing states
		losing_T = set()
		losing_S = set()

		for (f, v) in S:
			if v in flatten([G.edge_to_vertexpair[e] for e in node_to_face[f]]):
				losing_S.add((f,v))

		if len(T) == len(losing_T) or len(S) == len(losing_S):
			return False

		# Play the game
		while True:
			new_deletion = False

			for (e, C) in T:
				if all([(edge_to_node[e], v) in losing_S for v in C]):
					if (e, C) not in losing_T:
						new_deletion = True
						losing_T.add((e, C))

			for (e, C) in losing_T:
				f1 = edge_to_node[e]
				f2 = edge_to_node[-e]
				for (f, v) in [(f1, v) for v in C] + [(f2, v) for v in C]:
					if (f, v) not in losing_S:
						new_deletion = True
						losing_S.add((f, v))

			if len(T) == len(losing_T) or len(S) == len(losing_S):
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

	def linear_search_cw():
		k = 0
		while rat_wins(k):
			k += 1
		return k - 1

	cw = binary_search_cw()
	return cw

if __name__ == "__main__":
	adj = parse_text_to_adj()

	G = Graph()
	G.from_adj(adj)
	cw = carving_width(G)
	print("cw", cw)
