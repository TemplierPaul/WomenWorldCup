import pandas as pd
from urllib.request import Request, urlopen

#Merging ranking from the csv extracted from from the FIFA website (no API found)
def scraperRank():
    req = Request('https://www.fifa.com/fifa-world-ranking/ranking-table/women/', headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    df = pd.read_html(webpage)[0]
    df['Name'] = df['Team  Team'].str.split('  ', expand=True).drop(columns=[1])
    df['Soccerway_name'] = df["Name"].str.replace(' ', '-')
    df['Soccerway_name'] = df['Soccerway_name'].str.lower()
    print (df.columns)
    df = df.drop(columns=['Positions  Pos', 'Team  Team', 'Confederations  fifa_TBT'])
    df = df.rename(columns={
        'Rnk':'Rank',
        'Total Points  PTS':'Points',
        'Previous Points  Prev.Pts':'Previous_Points',
        'fifa_TBT':'+/-'
    })
    df.to_csv('ranking.csv')

def checkSoccerwayName():
    teams = pd.read_csv('ranking.csv', sep=',', index_col=0)
    errors = []
    print("Checking the generated Soccerway names"
          "**")
    for index, row in teams.iterrows():
        try:
            print(str(index) + " " + row['Name'])
            url = 'https://us.women.soccerway.com/teams/' + row['Soccerway_name'] + '/' + row[
                'Soccerway_name'] + '/matches/'
            m = pd.read_html(url)[0]
        except:
            try :
                url = 'https://us.women.soccerway.com/teams/' + row['Soccerway_name'] + '/' + \
                      row['Soccerway_name'] + '-' + row['Soccerway_name'] + '/matches/'
                m = pd.read_html(url)[0]
            except:
                print("##### ERROR #####")
                errors.append([row['Name'], row['Soccerway_name']])

    errors = pd.DataFrame(errors, columns=['Name', 'Soccerway_name'])
    print (errors)
    errors.to_csv("errors.csv")
    return errors

# Manually defined dictionary to correct Soccerway names
def manualNamesCorrection():
    rank = pd.read_csv('ranking.csv', sep=',', index_col=0)
    dict_replace = {
        'usa' : 'united-states',
        'republic-of-ireland':'ireland-republic',
        'ir-iran':'iran',
        'bosnia-and-herzegovina':'bosnia-herzegovina',
        'surniame':'surinam',
        'fyr-macedonia':'macedonia-fyr',
        'st.-kitts-and-nevis':'st-kitts-and-nevis',
        'eswatini':'swaziland'
            }
    rank = rank.replace(dict_replace)
    rank.to_csv('ranking.csv')

