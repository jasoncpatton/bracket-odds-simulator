from bs4 import BeautifulSoup
from urllib2 import urlopen
import re

fileout = 'kenpom_ratings.csv'

def get_kenpom():

    # Open KenPom.com and get the ratings table
    soup = BeautifulSoup(urlopen('http://kenpom.com'))
    table = soup.find('table', id='ratings-table').findAll('tr')

    # Grab AdjO, AdjD, and AdjT
    cols = ['AdjO', 'AdjD', 'AdjT']

    # Open local file
    with open(fileout, 'w') as f:
        f.write('Team,'+','.join(cols)+'\n')

        # Loop over the table and grab the ratings
        for tr in table:
            td = tr.find_all('td')
            if(td):

                # Remove seeding numbers from teams
                team = re.sub(r'[0-9]', '', td[1].get_text().rstrip()).rstrip()

                ratings = [float(x.get_text()) for x in td[5::2]]
                r = dict(zip(cols, ratings))

                f.write('%s,%.1f,%.1f,%.1f\n' % (team, r['AdjO'], r['AdjD'], r['AdjT']))

if __name__ == '__main__':
    get_kenpom()
    print 'Ratings written to %s' % (fileout)
