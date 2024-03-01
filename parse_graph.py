import networkx as nx
import sys

def parse_graph_to_nx():
	G = nx.MultiDiGraph()

	n = ord(sys.stdin.buffer.read(1))
	for i in range(n):
		G.add_node(i)
	i = 1
	while i <= n:
		x = ord(sys.stdin.buffer.read(1))
		if x == 0:
			i += 1
			continue
		G.add_edge(i-1, x-1)
	return G

def parse_graph_to_adj() -> dict[int, list[int]]:
	adj = dict()
	n = ord(sys.stdin.buffer.read(1))
	for i in range(1, n+1):
		adj[i] = []
	i = 1
	while i <= n:
		x = ord(sys.stdin.buffer.read(1))
		if x == 0:
			i += 1
			continue
		adj[i].append(x)
	return adj