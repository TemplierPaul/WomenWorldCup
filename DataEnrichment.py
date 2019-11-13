import pandas as pd
from FIFA_rank import *
from Match_history import *

"""
                CSV Files used : 

matches.csv

> addRank()

matches_with_rank.csv

> addRecentStats()

fully_enriched.csv

> doubleHistory()

data.csv

> addDifferences()

full_data.csv

"""

def addRank(prefix=''):
    matches = pd.read_csv(prefix + "matches.csv", sep=',', index_col=0)
    rank = pd.read_csv("unique.csv", sep=';', index_col=0)
    print('Matches columns: ', matches.columns)
    print('Ranking columns: ', rank.columns)
    df = pd.merge(matches, rank, how='left', left_on='A', right_on='Name_SW')
    df = pd.merge(df, rank, how='left', left_on='B', right_on='Name_SW', suffixes=('_A', '_B'))
    df = df.drop(columns=['Name_FIFA_A', 'Name_FIFA_B', 'Name_SW_A', 'Name_SW_B', 'Soccerway_name_A', 'Soccerway_name_B'])
    print('Data columns: ', df.columns)
    df.to_csv(prefix + "matches_with_ranks.csv")

def addRecentStats(prefix=''):
    matches = pd.read_csv("matches_with_ranks.csv", sep=',', index_col=0)
    if prefix !='':
        m = pd.read_csv(prefix + "matches_with_ranks.csv", sep=',', index_col=0)
        matches['Done']=1
        m['Done']=0
        matches = pd.concat([matches, m], sort=False)
        print('Concat: ', matches.columns)
        matches.to_csv('debug.csv')
    matches['Date'] = pd.to_datetime(matches['Date'])
    teams = pd.read_csv("unique.csv", sep=';', index_col=0)

    mA = matches[["Date", "A", "Score A", "Score B"]].copy()
    mA.columns = ["Date", "Team", "+", "-"]
    mB = matches[["Date", "B", "Score B", "Score A"]].copy()
    mB.columns = ["Date", "Team", "+", "-"]
    score_history = pd.concat([mA, mB], sort=False).sort_values('Date').reset_index(drop=True)
    print(str(len(score_history)) + ' scores')
    scores_with_mean = pd.DataFrame(columns=["Date", "Team", "+", "-", "Mean 3 +", "Mean 3 -"])

    for index, team in teams.iterrows():
        scores = score_history[score_history['Team'] == team['Name_SW']].copy()
        scores.sort_values('Date').reset_index(drop=True)
        scores["Mean 3 +"] = scores["+"].rolling(3).mean().shift(1)
        scores["Mean 3 -"] = scores["-"].rolling(3).mean().shift(1)
        scores_with_mean = pd.concat([scores_with_mean, scores], sort=False)
        # print (scores)

    data = pd.merge(matches, scores_with_mean, how="left", left_on=['Date', 'A'], right_on=["Date", 'Team'])
    data = pd.merge(data, scores_with_mean, how="left", left_on=['Date', 'B'], right_on=["Date", 'Team'],
                    suffixes=("_A", "_B"))
    data = data.fillna(0)
    print(str(len(data)) + ' fully enriched match results')

    if prefix != '':
        data = data[data['Done']==0].drop(columns=['Done'])
    data.to_csv(prefix + "fully_enriched.csv")

def doubleHistory (prefix=''):
    data = pd.read_csv(prefix + "fully_enriched.csv", index_col=0)
    data2 = data.copy()
    print(data2.columns)
    data2.columns = ['Day', 'Date', 'Competition', 'B', 'A', 'Score B', 'Score A',
                     'Rank_B', 'Points_B', 'Previous_Points_B', '+/-_B',
                     'Rank_A', 'Points_A', 'Previous_Points_A', '+/-_A',
                     'Team_B', '+_B', '-_B', 'Mean 3 +_B', 'Mean 3 -_B', 'Team_A', '+_A',
                     '-_A', 'Mean 3 +_A', 'Mean 3 -_A']

    data = pd.concat([data, data2], sort=False).sort_values('Date').reset_index(drop=True)
    data = data.drop(columns=['Team_A', 'Team_B'])
    data = data.sort_values('Date').reset_index(drop=True)
    print(str(len(data)) + ' match results in the ultimate dataset')
    data.to_csv(prefix + "data.csv")

def addDifferences (prefix=''):
    data = pd.read_csv(prefix + "data.csv", index_col=0)
    data['Score Difference'] = data['Score A'] - data['Score B']
    data['Points Difference'] = data['Points_A'] - data['Points_B']

    def win(r):
        d = r['Score A'] - r['Score B']
        if d == 0:
            return 1  # Draw
        if d < 0:
            return 2  # B wins
        if d > 0:
            return 0  # A wins

    data["Result"] = data.apply(win, axis=1)
    data.to_csv(prefix + "full_data.csv")


def fullEnrichmentFlow(scrap_FIFA=True, scrap_matches=False, prefix=''):
    if scrap_FIFA :
        scraperRank()                           # FIFA ranking
        # checkSoccerwayName()                  # Check whether the Soccer_name is correct, used to define manualNamesCorrection
        manualNamesCorrection()                    # Edit specific names
    if scrap_matches : scraperMatches()         # Match history


    print('Manual', pd.read_csv('ranking.csv', sep=',').columns)
    namesLink()                 # Linking FIFA names and SW names
    print('NamesLink', pd.read_csv('ranking.csv', sep=',').columns)
    addRank(prefix=prefix)                   # Add FIFA rank to match history
    addRecentStats(prefix=prefix)            # Compute stats of previous scores for each match
    doubleHistory(prefix=prefix)             # Use each match result as A-B and B-A
    addDifferences(prefix=prefix)            # Compute score and points differences
    print ('\n\n ### ' + prefix + 'matches has been enriched ###\n\n')



