# bandit_reranker


## Clone this Project
```sh
git clone https://github.com/chihming/bandit_reranker
```

## Prepare Data and Generate Environments for Reranking
```sh
bash prepare.sh
```
You'll get two .env data: `exp/dev.data.env` and `exp/test.data.env`. Each of them contains <user_id>\t<answer_ids>\t<recommendation_ids>
```
```


## Train and Evaluate
```sh
bash eval.sh
```
