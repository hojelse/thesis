import subprocess
import os
import time
import datetime
import logging

ns = [
	4,
	6,
	8,
	10,
	12,
	14,
	16,
	18,
	20,
	# 22,
	# 24,
]

start_time = time.time()

for n in ns:
	big_1 = (0, 'default')
	big_2 = (0, 'default')
	n_vertex_graph_files = sorted(os.listdir(f"./graphs/{n}"), key=lambda x: int(x.split(".")[0]))
	print(f"Checking {len(n_vertex_graph_files)} {n}-vertex graphs.")
	for i,file in enumerate(n_vertex_graph_files):
		if file.endswith(".bin"):

			seconds_elapsed = time.time() - start_time
			fraction_done = (i+1) / len(n_vertex_graph_files)
			logging.warning(f"{int(fraction_done * 100)}% elapsed: {str(datetime.timedelta(seconds=seconds_elapsed))} expected total time: {str(datetime.timedelta(seconds=(seconds_elapsed / fraction_done)))} remaining: {str(datetime.timedelta(seconds=(seconds_elapsed / fraction_done) - seconds_elapsed))}")

			file_name = f"./graphs/{n}/{file}"
			# print(file_name)
			with open(file_name, 'rb') as f:
				r = subprocess.run(['python3', 'count_hamcyc_faster.py'], stdin=f, text=True, capture_output=True)
				res = r.stdout.strip()

			lines = res.split("\n")
			size_1 = int(lines[0].split(" ")[0])
			if size_1 > big_1[0]:
				big_1 = (size_1, file_name)
			size_2 = int(lines[1].split(" ")[0])
			if size_2 > big_2[0]:
				big_2 = (size_2, file_name)
	print(big_1[0], big_2[0], 2**n, big_1[1], big_2[1])
