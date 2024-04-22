import networkx as nx
import sys

def parse_graph_to_nx():
	G = nx.MultiDiGraph()

	n = ord(sys.stdin.buffer.read(1))
	for i in range(n):
		G.add_node(i+1)
	i = 1
	while i <= n:
		x = ord(sys.stdin.buffer.read(1))
		if x == 0:
			i += 1
			continue
		G.add_edge(i, x)
	return G

def adj_to_nx(adj):
	G = nx.MultiDiGraph()
	for v,xs in adj.items():
		G.add_node(v)
		for x in xs:
			G.add_edge(v, x)
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

def adj_to_bytes(adj):
	print(chr(len(adj)), end="")
	for v,xs in adj.items():
		print("".join(map(chr, [*xs])), end="\x00")