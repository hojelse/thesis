from code.parse_graph import parse_graph_to_adj

for x,ys in parse_graph_to_adj().items():
	print(x, ' '.join(map(str, ys)))