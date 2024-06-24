import sys
from parse_graph import parse_graph_to_adj

def find_faces(adj: dict[int, list[int]]) -> list[list[(int, int)]]:
	# assume planar graph
	# assume adj is a rotation system
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

	def count_partitions(fixed_edge) -> int:
		vertex_subset_to_count = {(): 1}

		# filter out special faces
		def is_special_face(face):
			return fixed_edge in face or tuple(reversed(fixed_edge)) in face

		non_special_faces = list(filter(lambda face: not is_special_face(face), faces))

		coverable_vertices = [set()]
		for face in reversed(non_special_faces):
			coverable_vertices.append(coverable_vertices[-1].union(set(flatten(face))))
		coverable_vertices.reverse()

		def count_partitions_aux(i, vertices_to_be_covered) -> int:
			vertices_to_be_covered = tuple(sorted(vertices_to_be_covered))

			if vertices_to_be_covered in vertex_subset_to_count:
				return vertex_subset_to_count[vertices_to_be_covered]

			if len(set(vertices_to_be_covered).difference(coverable_vertices[i])) > 0:
				vertex_subset_to_count[vertices_to_be_covered] = 0
				return 0

			face = non_special_faces[i]

			legal_edges = (
				list(filter(lambda edge: edge[0] in vertices_to_be_covered and edge[1] in vertices_to_be_covered, face))
				if i < len(non_special_faces)
				else []
			)

			partitions_count = (
				sum([count_partitions_aux(i+1, tuple(set(vertices_to_be_covered).difference({u, v}))) for (u, v) in legal_edges])
				if len(legal_edges) > 0
				else 0
			)
			vertex_subset_to_count[vertices_to_be_covered] = partitions_count
			return partitions_count

		count = count_partitions_aux(0, vertex_set)

		return count
	
	vertex_set = set(adj.keys())
	faces = find_faces(adj)

	fixed_edges = [
		(1, adj[1][0]),
		(1, adj[1][1]),
		(1, adj[1][2])
	]

	count = 0

	for fixed_edge in fixed_edges:
		count += count_partitions(fixed_edge)

	return count // 2

adj = parse_graph_to_adj()
print(count_hamiltonian_cycles(adj))
