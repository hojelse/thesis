import random
import sys

VERTEX_COUNT = int(sys.argv[1])

N = 3
adj = {
	1: [2, 3],
	2: [3, 1],
	3: [1, 2]
}
faces = [(1, 2, 3)]

dual = {
	(3,2,1): [(1,2,3)],
	(1,2,3): [(3,2,1)]
}

while len(faces)+1 <= VERTEX_COUNT-2:
	# choose random face
	face = faces.pop(random.randint(0, len(faces)-1))

	N += 1

	# insert new vertex into face
	adj[N] = list(face)

	# insert neighbor in clockwise order
	a = face[0]
	b = face[1]
	c = face[2]
	adj[a].insert(adj[a].index(b)+1%3, N)
	adj[b].insert(adj[b].index(c)+1%3, N)
	adj[c].insert(adj[c].index(a)+1%3, N)

	# append new faces
	new_faces = [
		(a, b, N),
		(b, c, N),
		(c, a, N)
	]
	for new_face in new_faces:
		faces.append(new_face)

	# update dual
	for neighbor_face in dual[face]:
		face_idx = dual[neighbor_face].index(face)
		for new_face in new_faces:
			if new_face[0] in neighbor_face and new_face[1] in neighbor_face:
				dual[neighbor_face].insert(face_idx, new_face)
			elif new_face[1] in neighbor_face and new_face[2] in neighbor_face:
				dual[neighbor_face].insert(face_idx, new_face)
			elif new_face[2] in neighbor_face and new_face[0] in neighbor_face:
				dual[neighbor_face].insert(face_idx, new_face)
		dual[neighbor_face].remove(face)

	dual[new_faces[0]] = [new_faces[1], new_faces[2], *list(filter(lambda neighbor_face: a in neighbor_face and b in neighbor_face, dual[face]))]
	dual[new_faces[1]] = [new_faces[2], new_faces[0], *list(filter(lambda neighbor_face: b in neighbor_face and c in neighbor_face, dual[face]))]
	dual[new_faces[2]] = [new_faces[0], new_faces[1], *list(filter(lambda neighbor_face: c in neighbor_face and a in neighbor_face, dual[face]))]

	dual.pop(face, None)


faces = [(3,2,1), *faces]

face_to_id = dict([(face, i+1) for i,face in enumerate(faces)])

dual_ids = dict()
for k,v in dual.items():
	dual_ids[face_to_id[k]] = [face_to_id[x] for x in v]

with open(f"graphs_big/{len(faces)}.bin", 'wb') as f:
	f.write(len(faces).to_bytes(1, 'little'))
	for v,xs in dual_ids.items():
		for x in xs:
			f.write(x.to_bytes(1, 'little'))
		f.write(b'\x00')
