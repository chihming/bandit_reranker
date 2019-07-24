# bandit_reranker


## Clone this Project
```sh
git clone https://github.com/chihming/bandit_reranker
```

## Prepare Data and Generate Environments for Reranking
```sh
bash prepare.sh
```
You'll get two .env data: `exp/dev.data.env` and `exp/test.data.env`.
Each of them contains ``user_id``\t``answer_ids``\t``recommendation_ids`` likes:
```
68889   457 653 356 153 434     457 356 593 589 153 1 364 377 527 434 208 47 50 34 32 185 253 648 367 454
52509   711 76 135 32 708 736   135 9 637 743 88 694 762 61 12 74 736 260 724 653 839 32 3 102 1210 708
...   ...   ...
```
The reank task (i.e. `rerank.py`) is to rerank the <recommendation_ids> for matching <answer_ids>.

## Train and Evaluate
```sh
bash eval.sh
```
