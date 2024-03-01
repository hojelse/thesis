import subprocess
counts = {
	4: 1,
	6: 1,
	8: 3,
	10: 9,
	# 12: 37,
	# 14: 172,
	# 16: 993
}
for n,count in counts.items():
	for i in range(1, count+1):
		file_name = f'graphs/{n}/{i}.bin'
		print(file_name)
		with open(file_name, 'rb') as f:
			res1 = subprocess.run(['python3', 'count_hamcyc_brute_force.py'], stdin=f, text=True, capture_output=True)
		print(res1.stdout.strip())
		with open(file_name, 'rb') as f:
			res2 = subprocess.run(['python3', 'count_hamcyc_faster.py'], stdin=f, text=True, capture_output=True)
		print(res2.stdout.strip())
