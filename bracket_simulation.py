# Once a region is done with *all* of its games in a round,
# update the teams in that region by either deleting defeated teams
# or commenting them out with # at the beginning of the line.

# The number of simulations and update rate
# can also be changed on the command-line
n = 10000
update_rate = 1000

left_regions = ['south', 'west']    # Make sure these pairings are
right_regions = ['east', 'midwest'] # correct for the Final Four.

regions = left_regions + right_regions
rounds = ['R64', 'R32', 'S16', 'E8', 'F4', 'NCG']

fileout = 'simulation_results.txt'

# Initialize brackets and results for each region
brackets = {}
wins = {}

for region in regions:
    teams = []

    # each regional bracket is stored in <region>_bracket.txt
    try:
        for line in open('%s_bracket.txt' % (region)):
            if line[0] == '#': continue # skip commented teams

            line = line.rstrip()
            col = line.split(',')

            team = col[1] # team is stored in the second column
            teams.append(team)

            wins[team] = {}
            for rnd in xrange(len(rounds)):
                wins[team] = [0 for rnd in xrange(len(rounds))]

        brackets[region] = teams
    except IOError:
        print '''
-------------------------------------------------------
        One or more bracket files are missing
-------------------------------------------------------
'''
        raise

# Command-line parameters
from sys import argv
if len(argv) >= 2: n = int(argv[1])
if len(argv) >= 3: update_rate = int(argv[2])

# Load and define functions
from win_pct import win_pct
import numpy.random as random

# Determine the winner of a game
def get_game_winner((teamA, teamB)):

    threshold = win_pct(teamA, teamB)

    flip = random.rand()

    if flip < threshold:
        winner = teamA
    else:
        winner = teamB

    return winner

# Determine the results of a bracket
def get_bracket_winners((teams, round0), reseed = True):

    rnd = round0
    output = []

    # Make sure to reseed when doing multiprocessing
    if reseed: random.seed()

    while len(teams) > 1:

        winners = []
        for game in zip(teams[::2], teams[1::2]):
            winner = get_game_winner(game)
            output.append((winner, rnd))
            winners.append(winner)

        teams = winners
        rnd += 1

    return output

if __name__ == '__main__':

    # Open a multiprocessing pool
    from multiprocessing import Pool, cpu_count
    pool = Pool(min(len(regions), cpu_count()))

    # Get the current time
    from datetime import datetime
    time0 = datetime.now()

    # Run simulations
    from math import log
    for i in xrange(n):

        # Get teams and initial round from each region
        teams = [brackets[region] for region in regions]
        rnds0  = [-(int(log(len(regions),2)) + int(log(len(brackets[region]),2)))
                   for region in regions]

        # Compute regional brackets simulations
        winners = pool.map(get_bracket_winners, zip(teams, rnds0))

        # Store each teams' winnings
        teams = []
        for bracket in winners:
            for team, rnd in bracket:
                wins[team][rnd] += 1
            teams.append(bracket[-1][0]) # send surviving team to the Final Four

        # Compute Final Four bracket simulation
        rnd0 = -int(log(len(regions),2))
        winners = get_bracket_winners((teams, rnd0), reseed=False)

        # Store each teams' winnings
        for team, rnd in winners:
            wins[team][rnd] += 1

        # Give progress update
        if (i % update_rate == 0) and (i > 0) and (update_rate > 0):
            dt = (datetime.now() - time0)/(i+1)
            print '  %7.3f%% complete -' % (100*i/float(n)),
            print '%s per 1000 loops -' % (dt*1000),
            print '%s remaining' % (dt*(n-i))

    # Write output, sorted by teams' chance of winning the NCG
    teams = wins.keys()
    champ_sort = [[wins[team][rnd] for rnd in range(len(rounds))[::-1]] for team in teams]
    with open(fileout, 'w') as f:
        f.write('%20s\t%s\n' % ('n = %d' % (n), 'Chance to advance past each round'))
        f.write('%20s\t' % ('Team'))
        f.write('\t'.join(rounds) + '\n')
        for dummy,team in sorted(zip(champ_sort,teams), reverse=True):
            f.write('%20s\t' % (team))
            for rnd in range(len(rounds))[:-1]:
                if wins[team][rnd] == 0:
                    f.write('-\t')
                else:
                    f.write('%.2f%%\t' % (100*wins[team][rnd]/float(n)))
            f.write('%.2f%%\n' % (100*wins[team][-1]/float(n)))

    print 'Results written to %s' % (fileout)
