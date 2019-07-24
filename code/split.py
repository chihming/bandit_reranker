import os
import sys
import argparse
import random
import collections

PARSER = argparse.ArgumentParser(description="Parameters for the script.",
                                 usage="python -file [filename] -sep [splitter] -train_ratio [ratio] -exp [path_to_exp]")
PARSER.add_argument('-file', "--FILE", type=str,
                    default=None,
                    help="file name")
PARSER.add_argument('-sep', "--SPLITTER", type=str,
                    default='::',
                    help="line splitter")
PARSER.add_argument('-train_ratio', "--TRAIN_RATIO", type=float,
                    default=0.8,
                    help="training ratio")
PARSER.add_argument('-exp', "--EXP", type=str,
                    default='./exp',
                    help="exp folder")
PARSER.add_argument('-header', "--HEADER", type=int,
                    default=0,
                    help="if has header")
PARSER.add_argument('-columns', "--COLUMNS", type=str,
                    default='0,1,2',
                    help="columns of user, item, score")
PARSER.add_argument('-value_filter', "--VALUE_FILTER", type=float,
                    default=None,
                    help="filter value if lower than this")
PARSER.add_argument('-user_filter', "--USER_FILTER", type=float,
                    default=None,
                    help="filter user of lower than this")
PARSER.set_defaults(argument_default=False)
CONFIG = PARSER.parse_args()

def main():
    print('CONFIG:')
    print('\tfile = %s' % (CONFIG.FILE))
    print('\tsep = %s' % (CONFIG.SPLITTER))
    print('\theader = %d' % (CONFIG.HEADER))
    print('\tcolumn of user,item,value = %s' % (CONFIG.COLUMNS))
    print('\ttrain ratio = %f' % (CONFIG.TRAIN_RATIO))
    if CONFIG.VALUE_FILTER:
        print('\tfilter record has lower than %d value' % (CONFIG.VALUE_FILTER))
    if CONFIG.USER_FILTER:
        print('\tfilter user has lower than %d records' % (CONFIG.USER_FILTER))
    print('')

    print('Loading data from %s' % (CONFIG.FILE))
    u_col, i_col, v_col = list(map(int, CONFIG.COLUMNS.split(','))) # user, item, value
    records = collections.defaultdict(dict)
    with open(CONFIG.FILE, 'r') as f:
        if CONFIG.HEADER:
            next(f)
        for line in f:
            line = line.rstrip('\n').split('%s' % (CONFIG.SPLITTER))
            user = line[u_col]
            item = line[i_col]
            value = float(line[v_col])
            # filter value
            if CONFIG.VALUE_FILTER:
                if value < CONFIG.VALUE_FILTER:
                    continue
            records[user][item] = value
    # filter user
    if CONFIG.USER_FILTER:
        for user in list(records.keys()):
            if len(records[user]) < CONFIG.USER_FILTER:
                records.pop(user, None)
    
    # save train / test
    print('Splitting data')
    train_data_path = os.path.join(CONFIG.EXP, 'train.data')
    dev_data_path = os.path.join(CONFIG.EXP, 'dev.data')
    test_data_path = os.path.join(CONFIG.EXP, 'test.data')
    train_data = []
    dev_data = []
    test_data = []
    for eid, user in enumerate(records):
        items = list(records[user].keys())
        random.shuffle(items)
        cut_off = int(len(records[user])*CONFIG.TRAIN_RATIO)
        for item in items[:cut_off]:
            train_data.append('u%s i%s %f' % (user, item, records[user][item]))
        if eid % 5 != 0:
            for item in items[cut_off:]:
                dev_data.append('u%s i%s %f' % (user, item, records[user][item]))
        else:
            for item in items[cut_off:]:
                test_data.append('u%s i%s %f' % (user, item, records[user][item]))

    print('Saving train data to %s' % (train_data_path))
    with open(train_data_path, 'w') as f:
        f.write('%s\n' % ('\n'.join(train_data)))
    print('Saving dev data to %s' % (dev_data_path))
    with open(dev_data_path, 'w') as f:
        f.write('%s\n' % ('\n'.join(dev_data)))
    print('Saving test data to %s' % (test_data_path))
    with open(test_data_path, 'w') as f:
        f.write('%s\n' % ('\n'.join(test_data)))

if __name__=='__main__':
    main()
