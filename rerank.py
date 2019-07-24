import argparse
from collections import defaultdict
import bandit.bandit as bandit
from tqdm import tqdm

seed = 2019
PARSER = argparse.ArgumentParser(description="Parameters for the script.",
                                 usage="python -train [train_file] -test [test_file]")
PARSER.add_argument('-train', "--TRAIN", type=str,
                    default=None,
                    help="train file name")
PARSER.add_argument('-test', "--TEST", type=str,
                    default=None,
                    help="test file name")
PARSER.set_defaults(argument_default=False)
CONFIG = PARSER.parse_args()

def map_score(answers, recommendations):
    map_score = 0.
    match = 0.
    for pos, rec_id in enumerate(recommendations, 1):
        if rec_id in answers:
            match += 1
            map_score += match / pos
    map_score /= len(answers)
    return map_score

def train_bandit(_bandit, train_ans, train_arms, epoch=1):

    for _ in range(epoch):
        for user in tqdm(train_ans.keys()):
            answers = train_ans[user][:]
            arms = train_arms[user][:]
            for position in range(len(arms)):
                reward = 0.
                recommended_arm = _bandit.pull(arms)  # recommend an item
                del arms[arms.index(recommended_arm)] # remove the recommended item from pool
                if recommended_arm in answers:        # reward
                    reward = 1./(position+1.)
                _bandit.update(recommended_arm, reward)

def eval_bandit(_bandit, test_ans, test_arms):

    score = 0.
    for user in tqdm(test_ans):
        recommendations = []
        answers = test_ans[user][:]
        arms = test_arms[user][:]
        for position in range(len(arms)):
            recommended_arm = _bandit.pull(arms)  # recommend an item
            del arms[arms.index(recommended_arm)] # remove the recommended item from poo
            recommendations.append(recommended_arm)
        score += map_score(answers, recommendations)
    print('MAP:', score/len(test_ans))

def main():
    tested_bandits = [
        bandit.BaseBandit,
        bandit.RandomBandit,
        bandit.EpsilonGreedyBandit
    ]
    
    print('read training environment', CONFIG.TRAIN)
    train_ans = defaultdict(list)
    train_arms = defaultdict(list)
    observed_arms = {}
    with open(CONFIG.TRAIN, 'r') as f:
        for line in f:
            line = line.rstrip('\n').split('\t')
            user = line[0]
            answer = line[1].split(' ')
            arms = line[2].split(' ')
            train_ans[user] = answer[:]
            train_arms[user] = arms[:]
            for arm in answer+arms:
                observed_arms[arm] = 1
    observed_arms = list(observed_arms.keys())

    print('read testing environment', CONFIG.TEST)
    test_ans = defaultdict(list)
    test_arms = defaultdict(list)
    with open(CONFIG.TRAIN, 'r') as f:
        for line in f:
            line = line.rstrip('\n').split('\t')
            user = line[0]
            answer = line[1].split(' ')
            arms = line[2].split(' ')
            test_ans[user] = answer[:]
            test_arms[user] = arms[:]

    for tested_bandit in tested_bandits:
        _bandit = tested_bandit(observed_arms)
        print('train', _bandit)
        train_bandit(_bandit, train_ans, train_arms)
        print('evaluate', _bandit)
        eval_bandit(_bandit, test_ans, test_arms)
    

if __name__=='__main__':
    main()
