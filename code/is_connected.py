from parse_graph import parse_text_to_adj

G = parse_text_to_adj()

def is_connected(G):
	# make directed graph undirected
	es = set()
	for x,ys in G.items():
		for y in ys:
			es.add(tuple(sorted([x,y])))

	component_count = 0
	# DFS
	visited = set()
	for v in G.keys():
		if v not in visited:
			stack = [v]
			visited = set()
			while stack:
				v = stack.pop()
				visited.add(v)
				for u in G[v]:
					if u not in visited:
						stack.append(u)
			component_count += 1
	
	return component_count == 1

print(is_connected(G))
