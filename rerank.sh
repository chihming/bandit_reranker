set -x
# evaluate bandit reranker
python rerank.py -train ./exp/dev.data.env -test ./exp/test.data.env
