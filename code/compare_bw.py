import subprocess
import time
import datetime

ns = [10,14,18,22,26,30,34,38,42,46,50,54,58,62,66,70,74,78,82,86,90,94,98]

for n in ns:
	with open(f"../graphs/g/{n}-5.in", 'rb') as f:
		start_time = time.time()
		r = subprocess.run(['python3', 'branch_width.py'], stdin=f, text=True, capture_output=True)
		res = r.stdout.strip()
		seconds_elapsed = time.time() - start_time
		print(f"{n} {res} {str(datetime.timedelta(seconds=seconds_elapsed))}")
