for i in $(eval echo {0..$2})
do
	python3 render-graph.py $1 $i
done
