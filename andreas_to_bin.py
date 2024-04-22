import sys
from parse_graph import adj_to_bytes

adj = dict()

for i,line in enumerate(sys.stdin):
	adj[i+1] = list(map(lambda x: int(x)+1, line.strip().split()))

adj_to_bytes(adj)