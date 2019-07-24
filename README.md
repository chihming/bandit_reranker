# Bandit as Reranker!


## Clone this Project
```sh
git clone https://github.com/chihming/bandit_reranker
```

## Download Necessary Data / Tools, Setup Python Environment
Run this:
```sh
bash set.sh
```
To manually activate your python virtual environment, execute:
```sh
. ./bandit_env/bin/activate
```

## Prepare Data
Run this:
```sh
bash prepare.sh
```
You'll get train/dev/test data: `exp/train.data` / `exp/dev.data` / `exp/test.data`.
Each of them has the format [user_id]\t[item_id]\t[value] likes:
```
u68889 i588 4.000000
u68889 i292 4.000000
u11542 i1136 4.000000
u11542 i1240 4.000000
u11542 i1214 5.000000
```

### Generate Data Environments for Reranking (using Graph Embedding)
Run this:
```sh
bash train.sh
```
You'll get two .env data: `exp/dev.data.env` and `exp/test.data.env`.
Each of them has the format [user_id]\t[answer_ids]\t[recommendation_ids] likes:
```
u51268  i260 i104 i671 i135 i780 i480   i260 i32 i780 i653 i733 i494 i1073 i673 i788 i62 i104 i296 i112 i318 i135 i743 i150 i9 i12 i110
u29175  i500 i364 i587 i588 i318 i150   i150 i593 i318 i380 i296 i339 i474 i316 i592 i47 i50 i587 i440 i500 i350 i780 i588 i10 i364 i11
...   ...   ...
```
The reank task (i.e. `rerank.py`) is to rerank the <recommendation_ids> for matching <answer_ids>. The RL concept here is to select an **arm** from [recommendation_ids], and update its rewards.

## Train, Rerank and Evaluate
Run this:
```sh
bash rerank.sh
```
You'll get evalation results.

## Add NEW Bandit Method
1. inherit the base class in `bandit/bandit.py` 
2. call your created class in `rerank.py`
