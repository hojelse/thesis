for i in $(eval echo {0..$2})
do
	python3 create_png.py $1 $i
done
