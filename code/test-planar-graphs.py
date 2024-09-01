import math
import os
import subprocess
from subprocess import PIPE
import time

planar_graphs_dir = "./graphs/planar2/"
program = "branch_width.py"

files = os.listdir(planar_graphs_dir)
files.sort()

def run_command(file):
	process = None
	try:
		command = f"python3.12 {program} < {planar_graphs_dir}{file}"
		process = subprocess.Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
		stdout, stderr = process.communicate(timeout=2)
		if stderr:
			return f"Error encountered in {file}: {stderr.decode().strip()}"
		return stdout.decode().strip()
	except subprocess.TimeoutExpired:
		if process:
			process.terminate()
			try:
				process.wait(timeout=2)
			except subprocess.TimeoutExpired:
				process.kill()
		return f"Timeout in {file}"
	except Exception as e:
		if process:
			process.terminate()
			try:
				process.wait(timeout=5)
			except subprocess.TimeoutExpired:
				process.kill()
		return f"Exception in {file}: {e}"

for file in files:
	if file <= "007-001957.in":
		continue
	st = time.time()
	response = run_command(file)
	elapsed_time = time.time() - st

	formatted_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time)) + f".{int(elapsed_time * 1000) % 1000:03d}"
	n = int(file.split('-')[0])
	bw_bound = math.floor(4.5 * math.sqrt(n))

	print(f"{file};{n};{response.lstrip().strip()};{bw_bound};{formatted_time}")
