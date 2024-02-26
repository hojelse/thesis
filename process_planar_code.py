with open("planar_code.txt", "rb") as file:
	# skip header
	byte_count = 0
	while byte_count < 15:
		byte_s = file.read(1)
		if not byte_s:
			break
		byte_count += 1
	
	graph_idx = 0
	while True:
		byte_N = file.read(1)
		if not byte_N:
			exit()
		N = ord(byte_N)

		adj = file.read(N*4)
		
		with open(f"./graphs/{N}-{graph_idx}.bin", "xb") as outfile:
			outfile.write(byte_N)
			outfile.write(adj)
		graph_idx += 1
