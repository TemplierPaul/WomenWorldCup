import pandas as pd
from urllib import request
pd.options.display.max_columns = 100

def APImatchHistory(id):
    matches = pd.DataFrame(columns=['Day', 'Date', 'Competition', 'Outcome', 'Home team', 'Score/Time'])
    id = str(id)
    next = True
    i_n = 0
    while next :
        # print(i_n)
        try :
            n=str(i_n)
            url = 'https://us.women.soccerway.com/a/block_team_matches?block_id=page_team_1_block_team_matches_3&callback_params=%7B%22page%22%3A%22-' + n + '%22%2C%22block_service_id%22%3A%22team_matches_block_teammatches%22%2C%22team_id%22%3A%22' + id + '%22%2C%22competition_id%22%3A%220%22%2C%22filter%22%3A%22all%22%2C%22new_design%22%3A%22%22%7D&action=changePage&params=%7B%22page%22%3A-' + n + '%7D'
            # Calling the API and extracting the table into a Dataframe
            m = pd.read_html(pd.read_json(url)['commands'][0]['parameters']['content'])[0]
            m = m.drop(columns=['Away team', 'Unnamed: 7'])
            m = m.dropna()
            matches = pd.merge(matches, m, how='outer')
            i_n +=1
        except :
            next=False
            i_n=0

    # Selecting matches with final results only
    matches = matches[matches['Home team'].str.contains(' - ')]
    print(str(len(matches)) + " matches found")
    return matches

# Finding the id for each team
def findID(team):
    try :
        url = 'https://us.women.soccerway.com/teams/' + team + '/' + team + '/matches/'
        page = request.urlopen(url)
    except :
        try :
            url = 'https://us.women.soccerway.com/teams/' + team + '/' + team + '-' + team + '/matches/'
            page = request.urlopen(url)
        except :
            print("##### ID NOT FOUND #####")
            return False
    strpage = page.read().decode("utf-8")
    id = strpage.split('team_id')[1].split(':')[1].split(',')[0]
    return int(id)

# print(findID('andorra'))
# print(APImatchHistory(32925))
