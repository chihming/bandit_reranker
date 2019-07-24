import argparse
from collections import defaultdict
from multiprocessing import Queue
from multiprocessing import Process
import random

seed = 2019
PARSER = argparse.ArgumentParser(description="Parameters for the script.",
                                 usage="python -train [train_file] -test [test_file] -rep [rep_file] -cut [cut]")
PARSER.add_argument('-train', "--TRAIN", type=str,
                    default=None,
                    help="train file name")
PARSER.add_argument('-test', "--TEST", type=str,
                    default=None,
                    help="test file name")
PARSER.add_argument('-rep', "--REP", type=str,
                    default=None,
                    help="representation file name")
PARSER.add_argument('-worker', "--WORKER", type=int,
                    default=10,
                    help="number of worker")
PARSER.add_argument('-topk', "--TOPK", type=int,
                    default=20,
                    help="generate k recommendations")
PARSER.set_defaults(argument_default=False)
CONFIG = PARSER.parse_args()


def generate_recommendation(train_ans, test_ans, recommendation_pool, representation, user_ids, queue):
    def _dot(rep1, rep2):
        return sum([a*b for a,b in zip(rep1, rep2)])
    data = []
    for user in user_ids:
        answer = '%s' % (' '.join(list(test_ans[user].keys())))
        recommendation = []
        scores = defaultdict(lambda: 0.)
        
        uid = user
        for rid in recommendation_pool:
            if rid in train_ans[uid]: continue
            if uid in representation and rid in representation:
                score = _dot(representation[uid], representation[rid])
                if score < 0.:
                    continue
                scores[rid] = score

        retrievals = list(sorted(scores, key=scores.get, reverse=True))[:CONFIG.TOPK]
        queue.put('%s\t%s\t%s' % (user, answer, ' '.join(retrievals)))


def main():
    print('load train data from', CONFIG.TRAIN)
    train_ans = defaultdict(dict)
    users = {}
    items = {}
    recommendation_pool = {}
    with open(CONFIG.TRAIN, 'r') as f:
        for line in f:
            uid, iid, value = line.rstrip('\n').split(' ')
            train_ans[uid][iid] = 1
            users[uid] = 1
            items[iid] = 1
            recommendation_pool[iid] = 1

    print('load test data from', CONFIG.TEST)
    test_ans = defaultdict(dict)
    with open(CONFIG.TEST, 'r') as f:
        for line in f:
            uid, iid, value = line.rstrip('\n').split(' ')
            test_ans[uid][iid] = 1

    print("load representation from", CONFIG.REP)
    representation = {}
    with open(CONFIG.REP, 'r') as f:
        next(f)
        for line in f:
            line = line.rstrip('\n').split(' ')
            ID = line[0]
            fea = list(map(float, line[1:]))
            representation[ID] = fea

    print('generating recommendations')
    queue = Queue()
    procs = []
    recs = []

    workers=CONFIG.WORKER
    users = list(test_ans.keys())
    step = int(len(users)/workers + 1)
    start = 0
    end = step
    for p in range(workers):
        p = Process(target=generate_recommendation,
                    args=(train_ans, test_ans, recommendation_pool, representation, users[start:end], queue))
        start += step
        end += step
        end = min(end, len(users))
        
        procs.append(p)
        p.start()
    

    data = []
    counter = 0
    total_user = len(users)
    for counter in range(total_user):
        if counter % 1000 == 0:
            print("processed %d/%d (%.2f%%)" % (counter, total_user, counter/total_user*100))
        data.append("%s" % (queue.get()))

    for p in procs:
        p.join()

    print('write to %s' % (CONFIG.TEST+'.env'))
    with open(CONFIG.TEST+'.env', 'w') as f:
        f.write('%s\n' % ('\n'.join(data)))


if __name__=='__main__':
    main()


