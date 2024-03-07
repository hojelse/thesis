import sys
from parse_graph import parse_graph_to_adj

def find_faces(adj: dict[int, list[int]]) -> list[list[(int, int)]]:
	# assume planar graph
	# assume clockwise or counterclockwise ordering
	edges = set([(i, j) for i in adj for j in adj[i]])
	faces = []
	while len(edges) > 0:
		first_edge = edges.pop()
		v = first_edge[1]
		face = [first_edge]
		next_edge = first_edge
		while True:
			u = adj[next_edge[1]][(adj[next_edge[1]].index(next_edge[0])+1)%3]
			next_edge = (v, u)
			if next_edge == first_edge:
				faces.append(face)
				break
			edges.remove(next_edge)
			face.append(next_edge)
			v = u
	return faces

def flatten(xss):
	return [x for xs in xss for x in xs]

def count_hamiltonian_cycles(adj: dict[int, list[int]]) -> int:

	def count_partitions(covered_vertices, non_special_faces) -> int:
		covered_to_count = {(): 1}

		def count_partitions_aux(i, covered_vertices) -> int:
			covered_vertices = tuple(sorted(covered_vertices))
			if covered_vertices in covered_to_count:
				return covered_to_count[covered_vertices]

			face = non_special_faces[i]

			legal_edges = (
				list(filter(lambda edge: edge[0] in covered_vertices and edge[1] in covered_vertices, face))
				if i < len(non_special_faces)
				else []
			)

			partitions_count = (
				sum([count_partitions_aux(i+1, tuple(set(covered_vertices).difference({u, v}))) for (u, v) in legal_edges])
				if len(legal_edges) > 0
				else 0
			)
			covered_to_count[covered_vertices] = partitions_count
			return partitions_count

		count = count_partitions_aux(0, covered_vertices)

		return count
	
	vertex_set = set(adj.keys())
	faces = find_faces(adj)

	# fix an edge - assumes vertex 1 is in the graph
	fixed_edge = (1, adj[1][0])

	# filter out special faces
	def is_special_face(face):
		return fixed_edge in face or tuple(reversed(fixed_edge)) in face

	_non_special_faces = list(filter(lambda face: not is_special_face(face), faces))

	# count the number of hamiltonian cycles through the fixed edge
	count_through_fixed_edge = count_partitions(
		covered_vertices = vertex_set,
		non_special_faces = _non_special_faces
	)

	# count the number of hamiltonian cycles not through the fixed edge
	count_not_through_fixed_edge = count_partitions(
		covered_vertices = set(filter(lambda v: v not in fixed_edge, vertex_set)),
		non_special_faces = list(filter(lambda face: fixed_edge[0] not in flatten(face), _non_special_faces))
	)

	return count_through_fixed_edge + count_not_through_fixed_edge

adj = parse_graph_to_adj()
print(count_hamiltonian_cycles(adj))
