class Graph:
	def __init__(self):
		self.adj_edges: dict[int, list[int]] = dict()
		self.edge_to_vertexpair: dict[int, tuple[int, int]] = dict()
		pass

	def from_adj(self, adj: dict[int, list[int]]):
		# assign edge ids
		self.adj_edges = adj.copy()
		next_edgeid = 1
		for x, ys in self.adj_edges.items():
			for i,y in enumerate(ys):
				if x < y:
					self.edge_to_vertexpair[next_edgeid] = (x, y)
					self.edge_to_vertexpair[-next_edgeid] = (y, x)
					
					self.adj_edges[x][i] = next_edgeid
					self.adj_edges[y][adj[y].index(x)] = -next_edgeid

					next_edgeid += 1

	def incident_edges(self, v: int) -> list[int]:
		return self.adj_edges[v]

	def V(self) -> list[int]:
		return list(self.adj_edges.keys())
	
	def E(self) -> list[int]:
		return list(self.edge_to_vertexpair.keys())

	def N(self, v: int) -> list[int]:
		return [self.edge_to_vertexpair[e][1] for e in self.adj_edges[v]]

	def adj(self) -> dict[int, list[int]]:
		return dict([(x, self.N(x)) for x in self.adj_edges.keys()])
	
	def copy(self):
		H = Graph()
		H.adj_edges = self.adj_edges.copy()
		H.edge_to_vertexpair = self.edge_to_vertexpair.copy()
		return H
