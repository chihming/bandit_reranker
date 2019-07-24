import random

class BaseBandit(object):
    def __init__(self, arms):
        self.arms = arms

    def pull(self, given_arms=None):
        if given_arms:
            return given_arms[0]
        else:
            return random.choice(self.arms)

    def update(self, arm, reward):
        pass

    def __str__(self):
        return "BaseBandit"

class RandomBandit(BaseBandit):

    def pull(self, given_arms=None):
        if given_arms:
            return random.choice(given_arms)
        else:
            return random.choice(self.arms)

    def __str__(self):
        return "RandomBandit"


class EpsilonGreedyBandit(BaseBandit):
    def __init__(self, arms, epsilon=0.1):
        super(EpsilonGreedyBandit, self).__init__(arms)
        self.epsilon = epsilon
        self.values = [0. for _ in range(len(arms))]
        self.counts = [0. for _ in range(len(arms))]

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
                given_values = [self.values[self.arms.index(arm)] for arm in given_arms]
                max_index = given_values.index(max(given_values))
                return given_arms[max_index]
            else:
                max_index = self.values.index(max(self.values))
                return self.arms[max_index]

    def upadte(self, arm, reward):
        arm_index = self.arms.index(arm)
        self.counts[arm_index] += 1
        self.values[arm_index] += (reward - self.values[arm]) / self.counts[arm_index]

    def __str__(self):
        return "EpsilonGreedyBandit"

