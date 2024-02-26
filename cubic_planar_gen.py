import random

MIN_VERTEX_COUNT = 10

N = 3
embedding = [
	[50, 5],
	[5, 95],
	[95, 95]
]
adj = [
	[1, 2],
	[2, 0],
	[0, 1]
]

faces = [[0, 1, 2]]

for _ in range((MIN_VERTEX_COUNT-2)//2):
	# choose random face
	face = faces.pop(random.randint(0, len(faces)-1))

	# insert point
	x = N
	N += 1

	newX = (embedding[face[0]][0] + embedding[face[1]][0] + embedding[face[2]][0]) / 3
	newY = (embedding[face[0]][1] + embedding[face[1]][1] + embedding[face[2]][1]) / 3
	embedding.append([newX, newY])

	adj.append(face)

	a = face[0]
	b = face[1]
	c = face[2]
	adj[a].insert(adj[a].index(b)+1, x)
	adj[b].insert(adj[b].index(c)+1, x)
	adj[c].insert(adj[c].index(a)+1, x)

	# append new faces
	faces.append([a, b, x])
	faces.append([b, c, x])
	faces.append([c, a, x])

# print(N)
# for i,[x,y] in enumerate(embedding):
# 	print(i, x, y)
# for i,xs in enumerate(adj):
# 	print(i, *xs)

# calculate dual
faces = [[0,2,1], *faces]

dual_N = len(faces)
dual_embedding = []
dual_adj = [[] for _ in range(dual_N)]

for [a,b,c] in faces:
	newX = (embedding[a][0] + embedding[b][0] + embedding[c][0]) / 3
	newY = (embedding[a][1] + embedding[b][1] + embedding[c][1]) / 3
	dual_embedding.append([newX, newY])

for i,[a,b,c] in enumerate(faces):
	for j,other_face in enumerate(faces):
		if (i == j):
			continue
		if (a in other_face and b in other_face):
			dual_adj[i].append(j)
		if (a in other_face and c in other_face):
			dual_adj[i].append(j)
		if (b in other_face and c in other_face):
			dual_adj[i].append(j)

dual_embedding[0] = [50, 50]

print(dual_N)
for i,[x,y] in enumerate(dual_embedding):
	print(i, x, y)
for i,xs in enumerate(dual_adj):
	print(i, *xs)
