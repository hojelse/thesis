with open("planar_code.bin", "rb") as file:
	# skip header
	byte_count = 0
	while byte_count < 15:
		byte_s = file.read(1)
		if not byte_s:
			break
		byte_count += 1
	
	graph_idx = 1
	while True:
		byte_N = file.read(1)
		if not byte_N:
			exit()
		N = int.from_bytes(byte_N, byteorder='little')

		adj = file.read(N*4)
		
		with open(f"./graphs/{N}/{N}-{graph_idx}.bin", "xb") as outfile:
			outfile.write(byte_N)
			outfile.write(adj)
		graph_idx += 1
