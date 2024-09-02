import os

ns = [
	2, 3, 4, 5, 6,
]

for n in ns:
	os.system(f"./plantri.bin -pm1c1 {n} | python3 process_planar_code.py planar")