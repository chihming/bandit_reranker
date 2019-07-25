set -x
# split data
python code/split.py -file ./data/ml-10M100K/ratings.dat -sep '::' -train_ratio 0.8 -exp ./exp/ -header 0 -columns 0,1,2 -value_filter 3.5 -user_filter 5


