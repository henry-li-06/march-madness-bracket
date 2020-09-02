import numpy as np
import pandas as pd
import scrape_data
import csv

team_data = pd.read_csv('data/cbb19.csv')
team_data = team_data.drop(columns=['POSTSEASON', 'SEED'])
t = list(team_data['TEAM'])
all_games = scrape_data.all_games
winners = scrape_data.winners
name_mappings = {'UNC': 'North Carolina', 'Citadel': 'The Citadel', 'Purdue-Fort Wayne': 'Fort Wayne',
                 'Arkansas-Pine Bluff': 'Arkansas Pine Bluff', 'UT-Martin': 'Tennessee Martin', 'ETSU':
                 'East Tennessee St.', 'Gardner-Webb': 'Gardner Webb', 'UIC': 'Illinois Chicago', 'Louisiana-Monroe':
                 'Louisiana Monroe', 'Ole Miss': 'Mississippi', 'Prairie View': 'Prairie View A&M', "St. John's (NY)":
                 "St. John's", 'Miami (FL)': 'Miami FL', 'Miami (OH)': 'Miami OH', "Loyola (IL)": "Loyola Chicago",
                 "Loyola (MD)": "Loyola MD", "Pitt": "Pittsburgh", "Texas-Arlington": "UT Arlington",
                 "Alabama-Birmingham": "UAB", "St. Joseph's": "Saint Joseph's", 'Louisiana': 'Louisiana Lafayette',
                 'Omaha': 'Nebraska Omaha', 'California Baptist': 'Cal Baptist', 'Texas-Rio Grande Valley':
                 'UT Rio Grande Valley', 'Florida International': 'FIU', 'William ': 'William & Mary', 'UMass':
                 'Massachusetts', 'Saint Francis (PA)': 'St. Francis PA', 'LIU': 'LIU Brooklyn', 'Albany (NY)':
                 'Albany', 'St. Francis (NY)': 'St. Francis NY', 'Grambling': 'Grambling St.', 'Texas A&M-Corpus':
                 'Texas A&M Corpus Chris', 'UMass-Lowell': 'UMass Lowell', 'Bethune-Cookman': 'Bethune Cookman',
                 "St. Peter's": "Saint Peter's", "Maryland-Eastern Shore": "Maryland Eastern Shore", "SIU-Edwardsville":
                 "SIU Edwardsville"}

for i in range(len(all_games)):
    for j in range(len(all_games[0])):
        if('UC' in all_games[i][j]):
            if(all_games[i][j] == 'UCSB'):
                all_games[i][j] = 'UC Santa Barbara'
            elif(all_games[i][j] == "UConn"):
                all_games[i][j] = 'Connecticut'
            else:
                pos = all_games[i][j].find('-')
                if(pos != -1):
                    all_games[i][j] = all_games[i][j][:pos] + \
                        ' ' + all_games[i][j][pos+1:]
        elif('cal state' in all_games[i][j].lower()):
            pos = all_games[i][j].lower().find('state')
            all_games[i][j] = all_games[i][j][:pos] + \
                'St. ' + all_games[i][j][pos + 6:]
        elif('state' in all_games[i][j].lower()):
            if(all_games[i][j] == 'NC State'):
                all_games[i][j] = 'North Carolina St.'
            elif(all_games[i][j] == 'Bowling Green State'):
                all_games[i][j] = 'Bowling Green'
            elif(all_games[i][j] != "USC Upstate"):
                all_games[i][j] = all_games[i][j][:-3] + '.'
        elif(all_games[i][j] in name_mappings.keys()):
            all_games[i][j] = name_mappings[all_games[i][j]]

for i in range(len(winners)):
    if('UC' in winners[i]):
        if(winners[i] == 'UCSB'):
            winners[i] = 'UC Santa Barbara'
        elif(winners[i] == "UConn"):
            winners[i] = 'Connecticut'
        else:
            pos = winners[i].find('-')
            if(pos != -1):
                winners[i] = winners[i][:pos] + ' ' + winners[i][pos+1:]
    elif('cal state' in winners[i].lower()):
        pos = winners[i].lower().find('state')
        winners[i] = winners[i][:pos] + 'St. ' + winners[i][pos + 6:]
    elif('state' in winners[i].lower()):
        if(winners[i] == 'NC State'):
            winners[i] = 'North Carolina St.'
        elif(winners[i] == 'Bowling Green State'):
            winners[i] = 'Bowling Green'
        elif(winners[i] != "USC Upstate"):
            winners[i] = winners[i][:-3] + '.'
    elif(winners[i] in name_mappings.keys()):
        winners[i] = name_mappings[winners[i]]

games = pd.DataFrame(all_games, columns=['Away Team', 'Home Team'])
games['Winner'] = winners

games_to_drop = []
for i in range(len(games)):
    if(not(games['Away Team'][i] in t and games['Home Team'][i] in t)):
        games_to_drop.append(i)
games = games.drop(games_to_drop)

games = games.reset_index()
games = games.drop(columns=['index'])

with open('data/all_games_19.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['Away Team', 'Home Team', 'Winner'])
    for i in range(len(games)):
        writer.writerow(
            [games['Away Team'][i], games['Home Team'][i], games['Winner'][i]])
