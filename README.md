# bandit_reranker


## Clone this Project
```sh
git clone https://github.com/chihming/bandit_reranker
```

## Prepare Data
Run this:
```sh
bash prepare.sh
```
You'll get train/dev/test data: `exp/train.data` / `exp/dev.data` / `exp/test.data`.
Each of them has the format [user_id]\t[item_id]\t[value] likes:
```
58146 132 4.000000
68889 457 5.000000
68889 653 3.000000
```

### Generate Environments for Reranking
Run this:
```sh
bash train.sh
```
You'll get two .env data: `exp/dev.data.env` and `exp/test.data.env`.
Each of them has the format [user_id]\t[answer_ids]\t[recommendation_ids] likes:
```
68889   457 653 356 153 434     457 356 593 589 153 1 364 377 527 434 208 47 50 34 32 185 253 648 367 454
52509   711 76 135 32 708 736   135 9 637 743 88 694 762 61 12 74 736 260 724 653 839 32 3 102 1210 708
...   ...   ...
```
The reank task (i.e. `rerank.py`) is to rerank the <recommendation_ids> for matching <answer_ids>.

## Train and Evaluate
Run this:
```sh
bash eval.sh
```
You'll get evalation results.
