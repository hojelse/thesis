import math

from Graph import Graph
from parse_graph import parse_text_to_adj
from dual_graph import dual_graph

def carving_width(G: Graph) -> int:
	D, edge_to_link, link_to_edge, node_to_face, edge_to_node = dual_graph(G)

	# When the rat-catcher is on edge e, edge f is noisy iff there is
	# a closed walk of at most length k containing e* and f* in G* .
	# Return the un-noisy subgraph.
	def noisy_links(l: int, k: int) -> set[int]:
		s,t = D.edge_to_vertexpair[l]
		links = link_to_edge.keys()

		def dists(n: int) -> dict[int, int]:
			dist = {v: -1 for v in D.V()}
			dist[n] = 0
			stack = [n]
			while len(stack) > 0:
				v = stack.pop()
				for y in D.N(v):
					if dist[y] == -1:
						dist[y] = dist[v] + 1
						stack.append(y)
			return dist
		
		dist_s = dists(s)
		dist_t = dists(t)

		noisy = []
		for l in links:
			u,v = D.edge_to_vertexpair[l]
			if min(
				dist_s[u] + dist_t[v] + 2,
				dist_s[v] + dist_t[u] + 2
			) < k:
				noisy.append(l)

		return set([abs(e) for e in noisy])

	def quiet_links(l: int, k: int) -> set[int]:
		links = set([abs(e) for e in D.E()])
		return links - noisy_links(l, k)

	def quiet_edges(e: int, k: int) -> set[int]:
		return set([abs(link_to_edge[l]) for l in quiet_links(edge_to_link[e], k)])

	def quiet_components(e: int, k: int) -> dict[int, list[int]]:
		edges = quiet_edges(e, k)

		quiet_subgraph = {v: [] for v in G.V()}
		for e in edges:
			u,v = G.edge_to_vertexpair[e]
			quiet_subgraph[u].append(e)
			quiet_subgraph[v].append(-e)

		components = []
		unseen = set(quiet_subgraph.keys())

		while len(unseen) > 0:
			v = unseen.pop()
			component = [v]
			stack = [v]
			while len(stack) > 0:
				v = stack.pop()
				for e in quiet_subgraph[v]:
					u,v = G.edge_to_vertexpair[e]
					if v in unseen:
						unseen.remove(v)
						stack.append(v)
						component.append(v)
			components.append(component)

		# print("e", e, "(u,v)", G.edge_to_vertexpair[e], "k", k)
		# print("quiet_components", components)
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

		edge_set = edge_to_link.keys()

		
		Te = set([(e, tuple(C)) for e in edge_set for C in quiet_components(e, k)])
		Sr = set([(r, v) for r in node_to_face.keys() for v in G.V()])

		losing_eC = set()
		losing_rv = set()

		for (r, v) in Sr:
			if v in flatten([G.edge_to_vertexpair[e] for e in node_to_face[r]]):
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
				r2 = edge_to_node[-e]
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
			# print("trying", r)
			if rat_wins(r):
				l = r
				r *= 2
			else:
				break
		m = l
		while l < r:
			m = int(math.ceil((l + r) / 2))
			# print("trying", m)
			if rat_wins(m):
				l = m
			else:
				r = m - 1
		return l
	
	cw = binary_search_cw()
	return cw

if __name__ == "__main__":
	adj = parse_text_to_adj()

	G = Graph()
	G.from_adj(adj)
	cw = carving_width(G)
	print("cw", cw)
