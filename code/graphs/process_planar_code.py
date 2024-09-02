import sys
import os

def read_bin_to_adj() -> dict[int, list[int]]:
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

def adj_to_str(adj):
	s = str(len(adj)) + "\n"
	for v,xs in adj.items():
		s += str(v) + " " + " ".join(map(str, xs)) + "\n"
	return s

# skip header
byte_count = 0
while byte_count < 15:
	byte_s = sys.stdin.buffer.read(1)
	if not byte_s:
		break
	byte_count += 1

# read graphs
graph_idx = 1
while True:
	adj = read_bin_to_adj()

	folder_name = sys.argv[1]

	# create file if not exists
	if not os.path.exists(f"./{folder_name}"):
		os.makedirs(f"./{folder_name}")

	with open(f"./{folder_name}/{len(adj.keys()):03}-{graph_idx:06}.in", "w") as outfile:
		outfile.write(adj_to_str(adj))
	graph_idx += 1
