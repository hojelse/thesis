import networkx as nx

N = int(input())

G = nx.Graph()

for _ in range(N):
	v = int(input().split()[0])
	G.add_node(v)

for _ in range(N):
	xs = list(map(int, input().split()))
	v = xs[0]
	for x in xs[1:]:
		G.add_edge(v, x)

def is_3_regular(G):
	for v,xs in G.adjacency():
		if len(xs) != 3:
			return False
	return True

print("The graph is " + ("planar" if nx.is_planar(G) else "NOT planar") + " and " + ("cubic" if is_3_regular(G) else "NOT cubic"))
