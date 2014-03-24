import random
from itertools import accumulate

import matplotlib.pyplot as plt


def get_pick(pick_method, match):
    pick = None
    if pick_method == 'random':
        pick = random.choice([match.winner, match.loser])
    elif pick_method == 'favorite':
        pick = match.favorite()
    elif pick_method == 'underdog':
        pick = match.underdog()
    else:
        raise ValueError('winner method not properly specified')

    return pick


def simulate(matches, pick_method='random', num_sims=500, **kwargs):
    simulations = []
    for _ in range(num_sims):
        simulations.append(
            list(accumulate([match.calculate_reward(get_pick(pick_method, match), **kwargs) for match in matches])))

    return simulations


def plot_sims(simulations, colors):
    fig, ax = plt.subplots(figsize=(18, 12))
    fig.patch.set_facecolor('white')
    plt.subplots_adjust(wspace=0)

    ax1 = plt.subplot2grid((1, 3), (0, 0), colspan=2)
    ax1.set_xlim(right=len(simulations[0][0]))

    for sim_run, color in zip(simulations, colors):
        for run in sim_run:
            ax1.plot(run, linewidth=2, alpha=0.05, color=color)

    ax2 = plt.subplot2grid((1, 3), (0, 2))
    ax2.xaxis.tick_top()
    ax2.tick_params(axis='y', which='both', labelleft='off', labelright='on')
    ax2.set_ylim(ax1.get_ylim())

    for sim_run, color in zip(simulations, colors):
        ax2.hist([run[-1] for run in sim_run], normed=1, orientation='horizontal', color=color, alpha=0.6)

    ax2.autoscale(True, 'x', False)

    ax2.yaxis.set_label_position('right')
    ax2.xaxis.set_label_position('top')

    ax1.set_xlabel('Match Num')
    ax1.set_ylabel('Number of Items')
    ax2.set_xlabel('Probability')
    ax2.set_ylabel('Number of Items')

    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
    plt.show()


def plot_odds_correlation(groups, ratios, fidelity=2):
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.bar(groups, ratios, fidelity, color=(0.9, 0.9, 0.9))
    plt.plot([0, 100], [0, 1])
    ax.set_xlim(min(groups), max(groups) + fidelity)
    ax.set_xticks(groups + (max(groups) + fidelity,))
    ax.set_ylim(0, 1)
    ax.set_yticks([a / 10 for a in range(11)])
    ax.set_xlabel('Odds of the Favorite')
    ax.set_ylabel('Probability')
    fig.patch.set_facecolor('white')
    plt.show()


def plot_winners_vs_number_bets(num_bets,winner_odds):
    fig, ax = plt.subplots(figsize=(20,10))
    ax1 = plt.subplot2grid((1, 2), (0, 0))
    ax2 = plt.subplot2grid((1, 2), (0, 1))
    fig.patch.set_facecolor('white')
    ax1.plot(num_bets, winner_odds, 'ok')
    ax2.plot(num_bets, winner_odds, 'ok')
    ax2.set_xscale('log')
    ax1.set_xlabel('Number of Bettors')
    ax2.set_xlabel('Number of Bettors [Log Scale]')
    ax1.set_ylabel('Winner Odds')
    ax2.set_ylabel('Winner Odds')
    plt.show()