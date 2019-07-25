# train embeddings
./smore/cli/warp -train ./exp/train.data -save exp/rep.txt -dimensions 128 -sample_times 500 -alpha 0.1 -threads 8

# generate recommendations
python code/retrieve.py -train ./exp/train.data -test ./exp/dev.data -rep ./exp/rep.txt -worker 8 -topk 20
python code/retrieve.py -train ./exp/train.data -test ./exp/test.data -rep ./exp/rep.txt -worker 8 -topk 20

