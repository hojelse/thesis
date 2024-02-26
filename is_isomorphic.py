import networkx as nx

N = int(input())

G1 = nx.Graph()

for _ in range(N):
	v = int(input().split()[0])
	G1.add_node(v)

for _ in range(N):
	xs = list(map(int, input().split()))
	v = xs[0]
	for x in xs[1:]:
		G1.add_edge(v, x)

N = int(input())

G2 = nx.Graph()

for _ in range(N):
	v = int(input().split()[0])
	G2.add_node(v)

for _ in range(N):
	xs = list(map(int, input().split()))
	v = xs[0]
	for x in xs[1:]:
		G2.add_edge(v, x)

print("The graphs are " + ("isomorphic" if nx.is_isomorphic(G1, G2) else "NOT isomorphic"))
