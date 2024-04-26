import networkx as nx
import sys

def parse_bin_to_adj() -> dict[int, list[int]]:
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

def parse_text_to_adj() -> dict[int, list[int]]:
	adj = dict()
	n = int(input())
	for _ in range(n):
		ys = list(map(int, input().split()))
		x = ys[0]
		adj[x] = []
		for y in ys[1:]:
			adj[x].append(y)
	return adj

def adj_to_text(adj):
	print(len(adj))
	for v,xs in adj.items():
		print(v, *xs)

def adj_to_nx(adj):
	G = nx.MultiDiGraph()
	for v,xs in adj.items():
		G.add_node(v)
		for x in xs:
			G.add_edge(v, x)
	return G

def adj_to_bytes(adj):
	print(chr(len(adj)), end="")
	for v,xs in adj.items():
		print("".join(map(chr, [*xs])), end="\x00")