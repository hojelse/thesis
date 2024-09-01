import networkx as nx
from util import adj_from_stdin, adj_to_nx

G = adj_to_nx(adj_from_stdin())
print(nx.is_planar(G))
