import networkx as nx
from code.parse_graph import parse_graph_to_nx

G1 = parse_graph_to_nx()

G2 = parse_graph_to_nx()

print("The graphs are " + ("isomorphic" if nx.is_isomorphic(G1, G2) else "NOT isomorphic"))
