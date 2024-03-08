# Author: Andreas Björklund
from random import random
import sys

if len(sys.argv)>1:
  DEPTH=int(sys.argv[1])
else:  
  DEPTH=5
FRAC=0.9

def start_instance():
  # Original graph K_4  
  #   0
  #
  #   3
  #1     2
  C=[[2,3,1], [0,3,2], [1,3,0], [0,2,1]] 
  return C  
                         
# Generate random cubic 3-connected planar graph
def random_instance(C):
 
  # Triangle
  D=[[0,4,5],[1,5,3],[2,3,4]]
  
  # Single Bridge
  # 041
  # 253
  F=[[0,1,5],[2,4,3]]
  
  B = C[:]

  for rounds in range(1):
    n=len(B)
    who = int(random()*n)
    if random() < FRAC:
      nx = int(random()*3)
      cycle=[who]
      while B[who][nx]!=cycle[0]:
        cycle.append(B[who][nx])
        ix=[x for x in range(3) if B[B[who][nx]][x]==who]
        ix=(ix[0]+2)%3
        who = B[who][nx]
        nx = ix
    
      m=len(cycle)
      p = int(random()*(m-3))+2;
      T = cycle[:2] + cycle[p:p-2:-1]
      G = B[:]
      H = [(list(map(sum, zip(x, [n-4,n-4,n-4])))) for x in F]
      for i in range(4):
        for ix2 in range(3):
          if B[T[i]][ix2]==T[i^1]:
            G[T[i]]= (G[T[i]][:ix2]+[n+(i // 2)]+G[T[i]][ix2+1:])
        for j in range(len(F)):
          for k in range(3):
            if F[j][k]==i:
              H[j] = (H[j][:k]+[T[i]]+H[j][k+1:])
      B=G+H
    else:
      H = [(list(map(sum, zip(x, [n-3,n-3,n-3])))) for x in D]
      G = B[:]
      for i in range(3):
        for ix2 in range(3):
          if B[B[who][i]][ix2]==who:
            G[B[who][i]] = (G[B[who][i]][0:ix2]+[n+i]+G[B[who][i]][ix2+1:])
        for j in range(len(D)):
          for k in range(3):
            if D[j][k]==i:
              H[j] = (H[j][0:k]+[B[who][i]]+H[j][k+1:])
        
      B=G[:who]+G[who+1:]+H
    
      for j in range(len(B)):
        for k in range(3):
          if B[j][k]>who:
            B[j]=(B[j][:k]+[B[j][k]-1]+B[j][k+1:])
  return B

def gen_instance():
  C=start_instance()
  for i in range(DEPTH):
    C=random_instance(C)
  return C
  
C=gen_instance()
print(chr(len(C)), end="")
for i in range(len(C)):
  print("".join(map(chr, map(lambda i: i+1, C[i]))), end="\x00")