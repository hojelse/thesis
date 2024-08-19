import log
from branch_decomposition import branch_decomposition
from parse_graph import parse_text_to_adj, adj_to_text

def branch_width_of_branch_decomposition(bd):
	# Create an adjacency list from the branch decomposition
	T_adj = dict()
	def aux(subtree, depth, name):
		if len(subtree) == 2 and isinstance(subtree[0], int) and isinstance(subtree[1], int):
			T_adj[subtree] = []
			return subtree
		else:
			T_adj[name] = []
			for i,a in enumerate(subtree):
				child_name = aux(a, depth+1, name+str(i))
				T_adj[name].append(child_name)
				T_adj[child_name].append(name)
			return name
	aux(bd, 0, "i0")

	# Get the vertex set of the leafs of the subtree of x (not y)
	def leafs_set(x, y):
		leafs = set()
		visited = set([y])
		stack = [x]
		while stack:
			v = stack.pop()
			if isinstance(v, tuple):
				leafs.update(set(v))
				continue
			if v not in visited:
				visited.add(v)
				for w in T_adj[v]:
					stack.append(w)
		return leafs

	# Find the maximal width of any middle set
	width = 0
	for x,ys in T_adj.items():
		for y in ys:
			a = leafs_set(x, y)
			b = leafs_set(y, x)
			middle_set = len(a.intersection(b))
			width = max(width, middle_set)
	
	log.add("Branch width of branch decomposition: " + str(width))
	return width

def branch_width(adj: dict[int, list[int]]):
	bd = branch_decomposition(adj)
	bw = branch_width_of_branch_decomposition(bd)
	log.add("Branch width: " + str(bw))
	return bw

if __name__ == "__main__":
	adj = parse_text_to_adj()
	bd = branch_decomposition(adj)
	bw = branch_width_of_branch_decomposition(bd)
	print("bw", bw)
