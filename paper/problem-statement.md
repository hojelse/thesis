# Implementation of a minimal branch-decomposition algorithm of planar graphs.

Some graph optimization problems can be solved efficiently for graphs of small branchwidth. [Pin16]

Seymour and Thomas [ST93] give an algorithm, the rat-catching algorithm, on planar graphs for deciding bw(G) <= c in O(n^2) time, and by using it as a subroutine, a contraction algorithm to compute an optimal branch-decomposition in O(n^4) time.

Bian, Gub and Zhu [BGZ15] describes an implementation of this algorithm.

This paper will, with accessible and precise language, describe an implementation of the algorithm and have the source code published alongside it. Ideally also with a framework for testing correctness, and include a presentation of applications of the algorithm on problems like Counting Hamiltonian Cycles in 3-regular planar graphs and include results from running and comparing real-world performance with the theoretical run-time complexity.

- [ST93] Seymour and Thomas, "Call Routing and The Ratcatcher"
- [Pin16] W.J.A. Pino, "Cut and Count Representative Sets on Branch Decompositions"
- [BGZ15] Practical algorithms for branch-decompositions of planar graphs.pdf