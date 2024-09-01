import subprocess
import threading

expected = {
	f"python3 branch_width.py < ./graphs/random-planar-cubic/{10}-5.in": "3",
	f"python3 branch_width.py < ./graphs/random-planar-cubic/{14}-5.in": "3",
	f"python3 branch_width.py < ./graphs/random-planar-cubic/{18}-5.in": "4",
	f"python3 branch_width.py < ./graphs/random-planar-cubic/{22}-5.in": "4",
	f"python3 branch_width.py < ./graphs/random-planar-cubic/{26}-5.in": "4",
	f"python3 branch_width.py < ./graphs/random-planar-cubic/{30}-5.in": "4",
	f"python3 branch_width.py < ./graphs/random-planar-cubic/{34}-5.in": "4",
	f"python3 branch_width.py < ./graphs/random-planar-cubic/{38}-5.in": "5",
	f"python3 branch_width.py < ./graphs/random-planar-cubic/{42}-5.in": "5",
	f"python3 branch_width.py < ./graphs/random-planar-cubic/{46}-5.in": "5",
	f"python3 branch_width.py < ./graphs/random-planar-cubic/{50}-5.in": "5",
	f"python3 branch_width.py < ./graphs/random-planar-cubic/{54}-5.in": "5",
	f"python3 branch_width.py < ./graphs/random-planar-cubic/{58}-5.in": "5",
	f"python3 branch_width.py < ./graphs/random-planar-cubic/{62}-5.in": "5",
	f"python3 branch_width.py < ./graphs/random-planar-cubic/{66}-5.in": "5",
	f"python3 branch_width.py < ./graphs/random-planar-cubic/{70}-5.in": "5",
	f"python3 branch_width.py < ./graphs/random-planar-cubic/{74}-5.in": "5",
	f"python3 branch_width.py < ./graphs/random-planar-cubic/{78}-5.in": "5",
	f"python3 branch_width.py < ./graphs/random-planar-cubic/{82}-5.in": "5",
	f"python3 branch_width.py < ./graphs/random-planar-cubic/{86}-5.in": "5",
	f"python3 branch_width.py < ./graphs/random-planar-cubic/{90}-5.in": "5",
	f"python3 branch_width.py < ./graphs/random-planar-cubic/{94}-5.in": "5",
	f"python3 branch_width.py < ./graphs/random-planar-cubic/{98}-5.in": "6"
}

# Function to run a command
def run_command(cmd):
	process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
	stdout, stderr = process.communicate()
	if stdout:
		if stdout.strip() == expected[cmd]:
			print(f"Branch_width for {cmd}: {stdout.strip()} matches the expected output: {expected[cmd]}.")
		else:
			print(f"Branch_width for {cmd}: {stdout.strip()} does not match the expected output: {expected[cmd]}")
	if stderr:
		print(f"Error in {cmd}: {stderr}")

# Run the commands asynchronously
threads = []
for cmd in expected.keys():
	thread = threading.Thread(target=run_command, args=(cmd,))
	threads.append(thread)
	thread.start()

# Wait for all threads to complete
for thread in threads:
	thread.join()
