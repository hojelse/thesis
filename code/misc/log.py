import os
import sys
from Graph import Graph
from util import print_adj

def log_graph(graph: Graph, file_name: str):
	if len(sys.argv) > 1:
		graph_name = sys.argv[1]
		print("Logging to ./", graph_name, "/", file_name, sep="")
		if not os.path.exists(graph_name):
			os.makedirs(graph_name)

		with open(f"./{graph_name}/{file_name}", "w") as f:
			f.write(graph.to_lmg())

def log_adj(adj: dict[int, list[int | tuple[int, int]]], file_name: str):
	if len(sys.argv) > 1:
		graph_name = sys.argv[1]
		print("Logging to ./", graph_name, "/", file_name, sep="")
		if not os.path.exists(graph_name):
			os.makedirs(graph_name)

		with open(f"./{graph_name}/{file_name}", "w") as f:
			f.write(print_adj(adj))