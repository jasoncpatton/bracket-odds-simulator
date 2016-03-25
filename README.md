# bracket-odds-simulator

Set of Python scripts that 
simulates NCAA D-I Men's Basketball tournament brackets 
and reports the frequency of outcomes.
Using default files, 
it will simulate the 2016 NCAA Men's Basketball Championship,
but modifications can be made to match any D-I Men's Basketball tournament.
KenPom and Sagarin Predictor ratings
are used to determine a winning percentage for each matchup,
then outcomes are determined using NumPy's random number generator.

Requirements:
* Python 2.7
* NumPy
* SciPy
* Pandas
* BeautifulSoup

Usage:
1. Run sag2kenpom.py - builds the Sagarin to KenPom team name dictionary
2. Run get_kenpom.py and get_sagarin.py - grabs the latest KenPom and Sagarin ratings
3. Modify <region>_bracket.txt files (use provided files as examples)
4. Run bracket_simulation.py - simulates the tournament

Teams can either be removed or commented out from bracket files 
for simulating subsequent rounds.
The order of teams in the bracket files matters.
Teams should be paired based on their first round matchups.
See one of the provided files for example.

KenPom and Sagarin ratings can (and should) be updated 
by running get_kenpom.py and get_sagarin.py.

See the source code of bracket_simulation.py
for running this code for other tournaments (e.g. NIT).