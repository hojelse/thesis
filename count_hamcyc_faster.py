import networkx as nx
import matplotlib.pyplot as plt
import sys

def parse_graph() -> dict[int, list[int]]:
	adj = dict()
	n = ord(sys.stdin.buffer.read(1))
	for i in range(n):
		adj[i] = []
	i = 1
	while i <= n:
		x = ord(sys.stdin.buffer.read(1))
		if x == 0:
			i += 1
			continue
		adj[i-1].append(x-1)
	return adj

def find_faces(adj: dict[int, list[int]]) -> list[list[(int, int)]]:
	# assume planar graph
	# assume clockwise or counterclockwise ordering
	edges = set([(i, j) for i in adj for j in adj[i]])
	faces = []
	while len(edges) > 0:
		(first, v) = edges.pop()
		face = [(first, v)]
		next_edge = (first, v)
		while True:
			u = adj[next_edge[1]][(adj[next_edge[1]].index(next_edge[0])+1)%3]
			next_edge = (v, u)
			edges.remove(next_edge)
			face.append((v, u))
			v = u
			if v == first:
				faces.append(face)
				break
	return faces


adj = parse_graph()
N = len(adj)

# augment the graph with face vertices
def is_special_face(face):
	return fixed_edge in face or tuple(reversed(fixed_edge)) in face

faces = find_faces(adj)

# fix an edge
fixed_edge = (0, adj[0][0])

# Augmented graph - deep copy
aug_adj = dict([(k, [x for x in v]) for k,v in adj.items()])


# filter out special faces
non_special_faces = list(filter(lambda face: not is_special_face(face), faces))

face_vertices = [chr(i+ord('A')) for i in range(len(non_special_faces))]

# add face vertices
for i,face in enumerate(non_special_faces):
	x = face_vertices[i]
	aug_adj[x] = [a for (a, b) in face]
	for (a, b) in face:
		aug_adj[a].insert((aug_adj[a].index(b)+1)%3, x)

# triangles
triangles = sorted(set([(i, *sorted([j, k])) for i in face_vertices for j in aug_adj[i] for k in aug_adj[j] if i in aug_adj[k]]))

covered_to_count = {(): 1}
def count_ham_cycles(i=0, covered=([x for x in range(N)])) -> int:
	covered = tuple(sorted(covered))
	if covered in covered_to_count:
		return covered_to_count[covered]

	legal_edges = []
	if i < len(non_special_faces):
		legal_edges = list(filter(lambda p: p[0] in covered and p[1] in covered, non_special_faces[i]))

	count = 0
	if len(legal_edges) > 0:
		count = sum([count_ham_cycles(i+1, tuple(set(covered).difference({a, b}))) for (a, b) in legal_edges])

	covered_to_count[covered] = count
	return count

def flatten(xss):
	return [x for xs in xss for x in xs]

count_through_fixed_edge = count_ham_cycles()
# for k,v in covered_to_count.items():
# 	print(k, v)

# count the number of hamiltonian cycles not through the fixed edge
covered_to_count = {(): 1}
non_special_faces = list(filter(lambda face: fixed_edge[0] not in flatten(face), non_special_faces))
count_not_through_fixed_edge = count_ham_cycles(covered=[x for x in range(N) if x not in fixed_edge])

print(count_through_fixed_edge + count_not_through_fixed_edge)
print(f"through_fixed: {count_through_fixed_edge}, not_through_fixed: {count_not_through_fixed_edge}")
print(f"fixed edge: {fixed_edge}")

# render graph
# G = nx.DiGraph(adj)
# nx.draw(G, pos=nx.planar_layout(G), with_labels=True)
# plt.show()
