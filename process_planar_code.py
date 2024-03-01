import sys

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
	byte_N = sys.stdin.buffer.read(1)
	if not byte_N:
		exit()
	N = int.from_bytes(byte_N, byteorder='little')

	adj = sys.stdin.buffer.read(N*4)
	
	with open(f"./graphs/{N}/{graph_idx}.bin", "xb") as outfile:
		outfile.write(byte_N)
		outfile.write(adj)
	graph_idx += 1
