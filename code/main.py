import log
import branch_width
import sys
import Graph

graph_file_name = sys.argv[1]

log.init()
log.add("Reading graph from file " + graph_file_name)
with open(graph_file_name, 'r') as file:
	graph_str = file.read()

	G = Graph.Graph()
	if graph_file_name.endswith(".m.in"):
		G.from_lmg(graph_str)
	else:
		print("Unsupported file extension")
		exit()

	log.add("Graph: " + str(G))
	log.add("Graph adjacency list: " + str(G.adj()))

	bw = branch_width.branch_width(G.adj())
