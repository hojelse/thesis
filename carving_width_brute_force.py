from parse_graph import parse_graph_to_adj

G = parse_graph_to_adj()

def carving_width_brute_force(G: dict[int, list[int]]) -> bool:
	return min(carving_decomposition_width(G, cd) for cd in carving_decompositions(G))

def carving_decomposition_width(G: dict[int, list[int]], cd) -> int:
	root,t = cd
	width = 0
	for x, ys in t.items():
		for y in ys:
			width = max(width, partition_width(G, t, x, y))
	return width

def partition_width(G, t, x, y) -> int:
	root_x = x
	while True:
		stop = True
		for v in t[root_x]:
			if y == v:
				continue
			if len(v) > len(root_x):
				root_x = v
				stop = False
		if stop:
			break
	root_y = y
	while True:
		stop = True
		for v in t[root_y]:
			if x == v:
				continue
			if len(v) > len(root_y):
				root_y = v
				stop = False
		if stop:
			break

	smaller, vertex_set = (root_x, root_y) if len(root_x) < len(root_y) else (root_y, root_x)
	part1 = set(vertex_set) - set(smaller)
	part2 = set(smaller)

	count = 0

	for root_x in part1:
		for root_y in part2:
			if root_x in G[root_y]:
				count += 1
	return count

def carving_decompositions(G: dict[int, list[int]]):
	x = tuple(sorted(G.keys()))

	if len(x) == 2:
		x0 = tuple([x[0]])
		x1 = tuple([x[1]])
		return [(x0, {x0: [x1], x1: [x0]})]

	carvings = []
	for i in range(1, len(x)):
		for j in range(i+1, len(x)):
			l1 = x[:i]
			m1 = x[i:j]
			r1 = x[j:]
			for root_l, ts_l in carving_binary(l1):
				for root_m, ts_m in carving_binary(m1):
					for root_r, ts_r in carving_binary(r1):
						t = {
							x: [root_l, root_m, root_r],
							**ts_l,
							**ts_m,
							**ts_r,
						}
						t[root_l].append(x)
						t[root_m].append(x)
						t[root_r].append(x)
						carvings.append((x, t))
	return carvings

def carving_binary(x: tuple[int]):
	x = tuple(sorted(x))
	if len(x) == 1:
		return [(x, {x: []})]
	
	ts = []
	for i in range(1, len(x)):
		l = x[:i]
		r = x[i:]
		for root_l, ts_l in carving_binary(l):
			for root_r, ts_r in carving_binary(r):
				t = {
					x: [root_l, root_r],
					**ts_l,
					**ts_r,
				}
				t[root_l].append(x)
				t[root_r].append(x)
				ts.append((x, t))

	return ts


print("cw brute", carving_width_brute_force(G))