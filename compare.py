import subprocess
counts = {
	4: 1,
	6: 1,
	8: 3,
	10: 9,
	# 12: 38, # Errors on 22
	# 14: 178, # Errors on 85,89,91,98,102,113
	# 16: 1041
}
for n,count in counts.items():
	for i in range(1, count+1):
		file_name = f'graphs/{n}/{n}-{i}.bin'
		print(file_name)
		with open(file_name, 'rb') as f:
			res1 = subprocess.run(['python3', 'count_hamcyc_brute_force.py'], stdin=f, text=True, capture_output=True)
			print(res1.stdout.strip())
		with open(file_name, 'rb') as f:
			res2 = subprocess.run(['python3', 'count_hamcyc_faster.py'], stdin=f, text=True, capture_output=True)
			print(res2.stdout.strip())
