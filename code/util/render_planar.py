import matplotlib.pyplot as plt
import networkx as nx
from parse_graph import parse_graph_to_nx

G = parse_graph_to_nx()

nx.draw(G, pos=nx.planar_layout(G), with_labels=True)
plt.show()
