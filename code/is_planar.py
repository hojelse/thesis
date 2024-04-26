import networkx as nx
from parse_graph import parse_text_to_adj, adj_to_nx

G = adj_to_nx(parse_text_to_adj())
print(nx.is_planar(G))
