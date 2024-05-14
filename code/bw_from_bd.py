from code.branch_width.branch_width import branch_width_of_branch_decomposition
from parse_newick import parse_newick

s = input()
print(s)
nw = parse_newick(s)
print(nw)
bw = branch_width_of_branch_decomposition(nw)
print(bw)