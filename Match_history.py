import pandas as pd
from SoccerwayAPI import *

def scraperMatches():
    matches = pd.DataFrame(columns=['Day', 'Date', 'Competition', 'Outcome', 'Home team', 'Score/Time'])
    rank = pd.read_csv("ranking.csv", sep=",")

    for index, row in rank.iterrows():
        print("- " + str(index) + " " + row['Name'])
        # try:
        m = APImatchHistory(findID(row['Soccerway_name']))
        print(m.columns)
        # m.to_csv(row['Name'] + '.csv')
        matches = pd.concat([matches, m])
        # except:
        #     print("##### ERROR #####")
        print(str(len(matches)) + " total matches")

    matches = matches.rename(columns={'Outcome': 'A', 'Home team': 'Score', 'Score/Time': 'B'})

    # Splitting score into 2 columns
    matches['Score'] = matches['Score'].str.replace('E', '')
    matches['Score'] = matches['Score'].str.replace('P', '')
    new = matches['Score'].str.split(' - ', expand=True)
    matches['Score A'] = pd.to_numeric(new[0])
    matches['Score B'] = pd.to_numeric(new[1])
    matches = matches.drop(columns=['Score'])
    print(str(len(matches)) + ' match results scrapped')
    matches = matches.drop_duplicates()
    matches.to_csv("matches.csv")
    print(matches)
    print(matches.columns)
    print(str(len(matches)) + ' unique match results scrapped')
    return matches

# Linking FIFA names and SW names
def namesLink():
    rank = pd.read_csv("ranking.csv", sep=",", index_col=0)
    rank=rank.rename(columns={'Name':'Name_FIFA'})
    un = pd.DataFrame(pd.read_csv('matches.csv')['A'].unique())
    un.columns=['Name_SW']
    un['Soccerway_name'] = un["Name_SW"].str.replace(' ', '-')
    un['Soccerway_name'] = un['Soccerway_name'].str.lower()
    dict_replace = {
        'republic-of-ir…': 'ireland-republic',
        'trinidad-and-t…':'trinidad-and-tobago',
        "côte-d'ivoire":'cote-divoire',
        'uae':'united-arab-emirates',
        'north-macedonia':'macedonia-fyr',
        'st.-kitts-and-…':'st-kitts-and-nevis',
        'st.-vincent-/-…':'st.-vincent-and-the-grenadines',
        'eswatini':'swaziland',
        'antigua-and-ba…':'antigua-and-barbuda',
        'curaçao':'curacao'
    }
    un['Soccerway_name']=un['Soccerway_name'].replace(dict_replace)
    df = pd.merge(rank, un, how='left', on='Soccerway_name')
    df.to_csv('unique.csv', sep=";")
    return un

def groupStage():
    matches = pd.read_html('https://us.women.soccerway.com/international/world/womens-world-cup/2019-france/group-stage/r50993/matches/')[0]
    matches = matches.drop(columns=['Unnamed: 5', 'Unnamed: 6'])
    matches = matches.rename(columns={'Home team': 'A', 'Score/Time': 'Score', 'Away team': 'B'})
    matches['Score'] = '0 - 0'
    new = matches['Score'].str.split(' - ', expand=True)
    matches['Score A'] = pd.to_numeric(new[0])
    matches['Score B'] = pd.to_numeric(new[1])
    matches = matches.drop(columns=['Score'])
    matches['Competition']='WWC'
    matches = matches[['Day', 'Date', 'Competition', 'A', 'B', 'Score A', 'Score B']]
    matches['Date'] = pd.to_datetime(matches['Date'], dayfirst=True)
    matches = matches.sort_values('Date')
    matches.to_csv('group_stage_matches.csv')
