from pandas import read_csv
from scipy.stats import norm
import sys

# read ratings
try:
    df =         read_csv('kenpom_ratings.csv',  index_col=0)
    df = df.join(read_csv('sagarin_ratings.csv', index_col=0))
except IOError:
    print '''
-------------------------------------------------------
        One or more ratings files are missing
You may need to run get_kenpom.py and/or get_sagarin.py
-------------------------------------------------------
'''
    raise

sag_rmse = 8 # reverse engineered from rpiforecast.com
kpe = 11.5   # KenPom log5 exponent

def win_pct(teamA, teamB):
    
    (teamA, teamB) = (df.loc[teamA], df.loc[teamB])

    pythA = teamA['AdjO']**kpe / (teamA['AdjO']**kpe + teamA['AdjD']**kpe)
    pythB = teamB['AdjO']**kpe / (teamB['AdjO']**kpe + teamB['AdjD']**kpe)

    kpA = (pythA - pythA*pythB) / (pythA + pythB - 2*pythA*pythB)

    sagA = norm.sf(0, teamA['Predictor'] - teamB['Predictor'], sag_rmse)

    return sum([kpA, sagA])/2.

if __name__ == '__main__':
    print 'Some tests:'
    print '  Iowa St. (%.2f%%) vs. Kansas' % (win_pct('Iowa St.', 'Kansas')*100)
    print '  Duke (%.2f%%) vs. North Carolina' % (win_pct('Duke', 'North Carolina')*100)
    print '  Michigan (%.2f%%) vs. Ohio St.' % (win_pct('Michigan', 'Ohio St.')*100)
