from collections import defaultdict
import random

class BaseBandit(object):
    def __init__(self, arms):
        self.arms = arms

    def pull(self, given_arms=None):
        raise NotImplementedError("Not Implemented")

    def update(self, arm, reward):
        raise NotImplementedError("Not Implemented")

    def __repr__(self):
        raise NotImplementedError("Not Implemented")

class AlwaysFirstBandit(BaseBandit):

    def pull(self, given_arms=None):
        if given_arms:
            return given_arms[0]
        else:
            return random.choice(self.arms)

    def update(self, arm, reward):
        pass

    def __repr__(self):
        return "AlwaysFirstBandit"


class RandomBandit(BaseBandit):

    def pull(self, given_arms=None):
        if given_arms:
            return random.choice(given_arms)
        else:
            return random.choice(self.arms)

    def update(self, arm, reward):
        pass

    def __repr__(self):
        return "RandomBandit"


# FIXME: this implementation is slow
class EpsilonGreedyBandit(BaseBandit):
    def __init__(self, arms, epsilon=0.1, opt_value=0.):
        super(EpsilonGreedyBandit, self).__init__(arms)
        self.epsilon = epsilon
        self.opt_value = opt_value
        self.values = defaultdict(lambda: 0.)
        self.values.update({arm:self.opt_value for arm in self.arms})
        self.counts = defaultdict(lambda: 0.)
        self.counts.update({arm:0. for arm in self.arms})

    def pull(self, given_arms=None):
        # random case
        if random.random() < self.epsilon:
            if given_arms:
                return random.choice(given_arms)
            else:
                return random.choice(self.arms)
        # arg max
        else:
            if given_arms:
                given_values = {arm:self.values[arm] for arm in given_arms}
                max_arm = max(given_values, key=given_values.get)
                return max_arm
            else:
                max_arm = max(self.values, key=self.values.get)
                return max_arm

    def update(self, arm, reward):
        self.counts[arm] += 1
        self.values[arm] += (reward - self.values[arm]) / self.counts[arm]

    def __repr__(self):
        return "EpsilonGreedyBandit, epsilon=%.2f, opt_value=%.2f" % (
            self.epsilon, self.opt_value)

