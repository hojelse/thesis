class Graph:
	def __init__(self):
		self.adj_edges: dict[int, list[int]] = dict()
		self.edge_to_vertexpair: dict[int, tuple[int, int]] = dict()
		pass

	def from_adj(self, adj: dict[int, list[int]]):
		# assign edge ids
		adj_deepcopy = dict([(u, vs.copy()) for u, vs in adj.items()])
		self.adj_edges = adj_deepcopy
		next_edgeid = 1
		for x, ys in self.adj_edges.items():
			for i,y in enumerate(ys):
				if x < y:
					self.edge_to_vertexpair[next_edgeid] = (x, y)
					self.edge_to_vertexpair[-next_edgeid] = (y, x)
					
					self.adj_edges[x][i] = next_edgeid
					self.adj_edges[y][adj[y].index(x)] = -next_edgeid

					next_edgeid += 1

	def V(self) -> list[int]:
		return list(self.adj_edges.keys())
	
	def E(self) -> list[int]:
		return list(self.edge_to_vertexpair.keys())

	def N(self, v: int) -> list[int]:
		return [self.edge_to_vertexpair[e][1] if self.edge_to_vertexpair[e][0] == v else self.edge_to_vertexpair[e][0] for e in self.adj_edges[v]]

	def rename_vertex(self, old: int, new: int):
		self.adj_edges[new] = self.adj_edges.pop(old)
		for e in self.E():
			u,v = self.edge_to_vertexpair[e]
			if u == old:
				self.edge_to_vertexpair[e] = (new, v)
			if v == old:
				self.edge_to_vertexpair[e] = (u, new)

	def rename_edge(self, old: int, new: int):
		self.edge_to_vertexpair[new] = self.edge_to_vertexpair.pop(old)
		for u,vs in self.adj_edges.items():
			if old in vs:
				self.adj_edges[u][vs.index(old)] = new
	
	def adj(self) -> dict[int, list[int]]:
		return dict([(x, self.N(x)) for x in self.adj_edges.keys()])
	
	def copy(self):
		H = Graph()

		adj_edges_deepcopy = dict([(u, vs.copy()) for u, vs in self.adj_edges.items()])
		edge_to_vertexpair_deepcopy = dict([(e, t) for e, t in self.edge_to_vertexpair.items()])

		H.adj_edges = adj_edges_deepcopy
		H.edge_to_vertexpair = edge_to_vertexpair_deepcopy
		return H

	def from_lmg(self, input_string: str):
		lines = input_string.strip().split('\n')
		N, M = map(int, lines[0].split())

		for line in lines[1:N+1]:
			x, *ys = map(int, line.split())
			self.adj_edges[x] = ys

		for line in lines[N+1:]:
			e, u, v = map(int, line.split())
			self.edge_to_vertexpair[e] = (u, v)

	def to_lmg(self) -> str:
		s = str(len(self.adj_edges)) + " " + str(len(self.edge_to_vertexpair.keys())) + "\n"
		for x, ys in self.adj_edges.items():
			s += str(x) + " " + " ".join(map(lambda y: str(y), ys)) + "\n"
		for e, (u, v) in self.edge_to_vertexpair.items():
			s += str(e) + " " + str(u) + " " + str(v) + "\n"
		return s

	def __str__(self):
		return self.to_lmg()
	
def read_lmg_from_stdin() -> str:
	N,M = map(int, input().split())
	stdin_multiline_string = f"{N} {M}\n"
	for _ in range(N+M):
		stdin_multiline_string += input() + "\n"
	return stdin_multiline_string

def read_lmg_from_file(filename: str) -> str:
	with open(filename) as f:
		return f.read()

if __name__ == "__main__":
	G = Graph()
	G.from_lmg(read_lmg_from_stdin())
	print(G)