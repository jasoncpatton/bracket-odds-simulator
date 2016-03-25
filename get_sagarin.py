from bs4 import BeautifulSoup
from urllib2 import urlopen
import re
import cPickle as pickle
from datetime import datetime, timedelta

fileout = 'sagarin_ratings.csv'

def get_sagarin():

    # Get the pickled dict that converts Sagarin team names to KenPom
    try:
        sag2kenpom = pickle.load(open('sag2kenpom.pickle'))
    except IOError:
        print '''
-------------------------------------------------------
    Sagarin to KenPom team names pickle missing
         You may need to run sag2kenpom.py
-------------------------------------------------------
'''
        raise

    # Define some regexps to extract teams and ratings
    teamfind = re.compile('[0-9;]  (.*)=')
    ratingfind = re.compile('([0-9]{2,3}\.[0-9]{2})')

    # Get the current year (next year in Nov/Dec)
    year = (datetime.now() + timedelta(days=62)).year

    # Open the current ratings
    soup = BeautifulSoup(urlopen('http://www.usatoday.com/sports/ncaab/sagarin/%d/team/' % (year)))

    team0 = ''

    # Open local file
    with open(fileout, 'w') as f:

        f.write('Team,Predictor\n')

        # Loop over where ever BeautifulSoup finds a team
        for teamhtml in soup('font', {'color': '#000000'}, text=teamfind):

            team = teamhtml.get_text()
            team = teamfind.search(team).group(1).rstrip()

            # Check if this is actually a new team
            if(not team or team == team0): continue
            if(team in sag2kenpom.keys()): team = sag2kenpom[team]

            # Find the Predictor rating (blue text)
            ratinghtml = teamhtml.find_next_sibling('font', {'color': '#0000ff'}, text=ratingfind)
            if(not ratinghtml): continue
            rating = ratinghtml.get_text()
            rating = float(ratingfind.search(rating).group(1))

            f.write('%s,%.2f\n' % (team, rating))

            team0 = team

if __name__ == '__main__':
    get_sagarin()
    print 'Ratings written to %s' % (fileout)
