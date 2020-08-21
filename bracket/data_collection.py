import bs4
from bs4 import BeautifulStoneSoup
from requests import get
import urllib
import calendar

def getTeam(s):
    s.encode('ascii', 'ignore')
    pos1 = s.find('\n')
    pos2 = lastChar(s[pos1+1:])
    return s[pos1+1:pos2+1]

def lastChar(s):
    for i in range(len(s)):
        if((not (s[i:i+1].isalnum() or s[i:i+1] == ' '))  \
           and s[i:i+1] != '-' and s[i:i+1] != '(' and s[i:i+1] != '.' \
           and s[i:i+1] != "'" and s[i:i+1] != ")" and s[i:i+1] != "&"):
            return i


month = 11
day = 6
year = 2018
all_games = []
winners = []
while((year < 2019 and month <= 12) or (month <= 2019 and month <= 2)):
    while(day < calendar.monthrange(year,month)[1]):
        url = 'https://www.sports-reference.com/cbb/boxscores/index.cgi?month=' + str(month) + '&day=' + str(day) + '&year=' + str(year)
        response = get(url)
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        summaries = soup.find_all('div', {'class': 'game_summary'})
        for game_summary in summaries:
            game = []
            teams = game_summary.find_all('tr', {'class': ['winner', 'loser']})
            for team in teams:
                game.append(getTeam(team.text))
            winners.append(getTeam(game_summary.find('tr', {'class': 'winner'}).text))
            all_games.append(game)
        day += 1
    if(month == 12 and day == 31):
        year += 1
    if(month < 12):
        month += 1
    else:
        month = 1
    day = 1

days_map = {3: 31, 4: 9}
month = 3
day = 19
mm_games = []
mm_winners = []
while(day <= days_map[month]):
    url = 'https://www.sports-reference.com/cbb/boxscores/index.cgi?month=' + str(month) + '&day=' + str(day) + '&year=2019'
    response = get(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    summaries = soup.find_all('div', {'class': 'game_summary'})
    # some loop to get scores
    for game_summary in summaries:
        game = []
        teams = game_summary.find_all('tr', {'class': ['winner', 'loser']})
        for team in teams:
            game.append(getTeam(team.text))
        #summary = game_summary.find('div', {'class': 'game_summary'})
        # print(str(month) + '/' + str(day))
        if('NCAA' in game_summary.find_all('tr')[2].text):
            mm_winners.append(getTeam(game_summary.find('tr', {'class': 'winner'}).text))
            mm_games.append(game)
    # also need some way to successfully iterate through days 
    day += 1
    if(month == 3 and day == 31):
        month += 1
        day = 1
    




