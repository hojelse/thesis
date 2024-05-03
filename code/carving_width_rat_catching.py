from parse_graph import parse_text_to_adj
from dual_graph import dual_graph
import math

def carving_width_rat_catching(G) -> int:
	D, _D, linkid_to_nodepair, edgeid_to_linkid, linkid_to_edgeid, nodeid_to_edgeids, edgeid_to_nodeid, edgeid_to_vertexpair,_,_ = dual_graph(G)


	# When the rat-catcher is on edge e, edge f is noisy iff there is
	# a closed walk of at most length k containing e* and f* in G* .
	# Return the un-noisy subgraph.
	def noisy_links(l: int, k: int) -> set[int]:
		s,t = linkid_to_nodepair[l]
		noisy = set()
		def bfs(walk_acc: list[int]):
			if len(walk_acc) == k: return
			v = linkid_to_nodepair[walk_acc[-1]][1]
			if v == s:
				noisy.update(walk_acc)
			for e in _D[v]:
				bfs(walk_acc + [e])
		bfs([l])
		return set([abs(e) for e in noisy])

	def quiet_links(l: int, k: int) -> set[int]:
		links = set([abs(e) for e in linkid_to_nodepair.keys()])
		return links - noisy_links(l, k)

	def quiet_edges(e: int, k: int) -> set[int]:
		return set([abs(linkid_to_edgeid[l]) for l in quiet_links(edgeid_to_linkid[e], k)])

	def quiet_components(e: int, k: int) -> dict[int, list[int]]:
		edges = quiet_edges(e, k)

		quiet_subgraph = {v: [] for v in G.keys()}
		for e in edges:
			u,v = edgeid_to_vertexpair[e]
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
					u,v = edgeid_to_vertexpair[e]
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
		if len(G) < 2:
			return False
		
		if max([len(G[v]) for v in G]) >= k:
			return True

		edge_set = edgeid_to_linkid.keys()

		Te = set([(e, tuple(C)) for e in edge_set for C in quiet_components(e, k)])
		Sr = set([(r, v) for r in nodeid_to_edgeids.keys() for v in G.keys()])

		losing_eC = set()
		losing_rv = set()

		for (r, v) in Sr:
			if v in flatten([edgeid_to_vertexpair[e] for e in nodeid_to_edgeids[r]]):
				losing_rv.add((r,v))

		if len(Te) == len(losing_eC) or len(Sr) == len(losing_rv):
			return False

		while True:
			new_deletion = False

			for (e, C) in Te:
				if all([(edgeid_to_nodeid[e], v) in losing_rv for v in C]):
					if (e, C) not in losing_eC:
						new_deletion = True
						losing_eC.add((e, C))
			
			for (e, C) in losing_eC:
				r1 = edgeid_to_nodeid[e]
				r2 = edgeid_to_nodeid[-e]
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

if __name__ == "__main__":
	G = parse_text_to_adj()
	cw = carving_width_rat_catching(G)
	print("cw is", cw)
