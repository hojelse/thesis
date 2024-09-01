def adj_from_stdin() -> dict[int, list[int]]:
	adj = dict()
	n = int(input())
	for _ in range(n):
		ys = list(map(int, input().split()))
		x = ys[0]
		adj[x] = []
		for y in ys[1:]:
			adj[x].append(y)
	return adj

# The branchwidth of G is the minimum width of any of its branch-decompositions.
def branch_width(G):
	Ts = branch_decompositions(G)
	min_T = min(Ts, key=width_of_branch_decomposition)
	print(min_T)
	return width_of_branch_decomposition(min_T)

# A branch-decomposition of a graph G is a tree T such that:
# - The leafs of T are the edges of G.
# - The internal nodes of T have 3 neighbors.
def branch_decompositions(G):
	leaves = [f"{chr(64 + i)}{chr(64 + j)}" for (i, j) in edges(G)]
	trees = enumerate_trees(leaves)
	return [tree.to_adj() for tree in trees]

# The width of a branch-decomposition T is the maximum width of any of its e-separations.
def width_of_branch_decomposition(T):
	return max(width_of_e_seperation(T, e) for e in edges(T))

def edges(T):
	edge_set = set()
	for v in T:
		for w in T[v]:
			edge_set.add(tuple(sorted((v, w))))
	return edge_set

# The width of an e-separation is the number of vertices of G that appear in both T1 and T2.
def width_of_e_seperation(T, e):
	S1 = leafs_of(T, e[0], e[1])
	S2 = leafs_of(T, e[1], e[0])
	return len(set(S1).intersection(S2))

def leafs_of(T, s, x):
	seen = set([x])
	leafs = []
	stack = [s]
	while stack:
		v = stack.pop()
		if v in seen:
			continue
		seen.add(v)
		if "internal" not in v:
			leafs.extend(list(v))
		stack.extend(T[v])
	return leafs

# Enumerate trees, https://github.com/fedeoliv/Rosalind-Problems/blob/master/eubt.py
# solving https://rosalind.info/problems/eubt/
class Node():
	def __init__(self, name):
		self.name = name

	def __str__(self):
		if self.name is not None:
			return self.name
		else:
			return "internal_{}".format(id(self))

class Edge():
	def __init__(self, node1, node2):
		self.nodes = [node1, node2]

	def __str__(self):
		return "{}--{}".format(*self.nodes)

class Tree():
	def __init__(self, nodes=[], edges=[]):
		self.nodes = nodes
		self.edges = edges

	def __str__(self):
		return "tree_{} edges: {}".format(id(self), [str(x) for x in self.edges])

	def copy(self):
		node_conversion = {node: Node(node.name) for node in self.nodes}
		new_nodes = list(node_conversion.values())
		new_edges = [Edge(node_conversion[edge.nodes[0]], node_conversion[edge.nodes[1]]) for edge in self.edges]

		new_tree = Tree(new_nodes, new_edges)
		return new_tree
	
	def to_adj(self):
		adj = {}
		for node in self.nodes:
			adj[str(node)] = []
		for edge in self.edges:
			node1, node2 = edge.nodes
			adj[str(node1)].append(str(node2))
			adj[str(node2)].append(str(node1))
		return adj

def enumerate_trees(leaves):
	assert(len(leaves) > 1)
		
	if len(leaves) == 2:
		n1, n2 = leaves
		t = Tree()
		t.nodes = [Node(n1), Node(n2)]
		t.edges = [Edge(t.nodes[0], t.nodes[1])]
		return [t]
	elif len(leaves) > 2:
		# get the smaller tree first
		old_trees = enumerate_trees(leaves[:-1])
		new_leaf_name = leaves[-1]
		new_trees = []

		# find the ways to add the new leaf
		for old_tree in old_trees:
			for i in range(len(old_tree.edges)):
				new_tree = old_tree.copy()
				edge_to_split = new_tree.edges[i]
				old_node1, old_node2 = edge_to_split.nodes

				# get rid of the old edge
				new_tree.edges.remove(edge_to_split)

				# add a new internal node
				internal = Node(None)
				new_tree.nodes.append(internal)

				# add the new leaf
				new_leaf = Node(new_leaf_name)
				new_tree.nodes.append(new_leaf)

				# make the three new edges
				new_tree.edges.append(Edge(old_node1, internal))
				new_tree.edges.append(Edge(old_node2, internal))
				new_tree.edges.append(Edge(new_leaf, internal))

				# put this new tree in the list
				new_trees.append(new_tree) 

		return new_trees

adj = adj_from_stdin()

print(branch_width(adj))