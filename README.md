# Count Hamilonian Cycles in Simple Connected Planar Cubic Graphs

`count_ham_cyc_brute_force.py` runs in O(N!) time.

`count_ham_cyc_faster.py` run in O(2^N * poly(N)) time.

## Test

### Generate all Simple Connected Planar Cubic Graphs in a single binary file. https://github.com/mishun/plantri

Example
`./plantri -c1ad 8`

### Generate all n-vertex Simple Connected Planar Cubic Graphs in seperate files.

Example
`./gen_all_n_vertex_graphs.sh 8`

### Validate test cases

Example
`python3 validate_simple_cubic_planar.py < graphs/8/1.bin`

Example
`cat graphs/8/1.bin graphs/8/2.bin | python3 is_isomorphic.py`

### Compare answers between `count_ham_cyc_brute_force.py` and `count_ham_cyc_faster.py`

Example
`python3 compare.py`

### Create pngs of graphs

Example
`python3 create_png.py < graphs/8/1.bin`

### Test cache sizes

`python3 test.py`