import itertools
import random

import matplotlib.pyplot as plt

from pyd2l.match import Match, InvalidMatchError


def main():
    matches = []

    for match_id in range(500, 601):
        try:
            matches.append(Match(match_id))
        except InvalidMatchError:
            pass

    for _ in range(30):
        plt.plot([0] + list(itertools.accumulate(
            [match.calculate_reward(random.choice([match.winner, match.loser]), reward_round=True) for match in matches])), 'k', alpha=0.5)

    plt.show()


if __name__ == "__main__":
    main()