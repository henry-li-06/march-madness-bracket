import pandas as pd
import numpy as np
import csv
from sklearn.preprocessing import StandardScaler, MinMaxScaler

all_games_19 = pd.read_csv('data/all_games_19.csv')
mm_games_19 = pd.read_csv('data/mm_games_19.csv')
team_data = pd.read_csv('data/cbb19.csv')

all_games_19['t1_points'] = 0.0
all_games_19['t2_points'] = 0.0
all_games_19['Away Win'] = 'N'

mm_games_19['t1_points'] = 0.0
mm_games_19['t2_points'] = 0.0
mm_games_19['Away Win'] = 'N'

for i in range(len(all_games_19)):
    if (all_games_19['Away Team'][i] == all_games_19['Winner'][i]):
        all_games_19['Away Win'][i] = 'Y'
    all_games_19['t1_points'][i] = team_data.loc[
        team_data['TEAM'] == all_games_19['Away Team'][i],
        ['ADJOE']].reset_index()['ADJOE'][0] + team_data.loc[
            team_data['TEAM'] == all_games_19['Home Team'][i],
            ['ADJDE']].reset_index()['ADJDE'][0]
    all_games_19['t2_points'][i] = team_data.loc[
        team_data['TEAM'] == all_games_19['Home Team'][i],
        ['ADJOE']].reset_index()['ADJOE'][0] + team_data.loc[
            team_data['TEAM'] == all_games_19['Away Team'][i],
            ['ADJDE']].reset_index()['ADJDE'][0]

for i in range(len(mm_games_19)):
    if (mm_games_19['Away Team'][i] == mm_games_19['Winner'][i]):
        mm_games_19['Away Win'][i] = 'Y'
    mm_games_19['t1_points'][i] = team_data.loc[
        team_data['TEAM'] == mm_games_19['Away Team'][i],
        ['ADJOE']].reset_index()['ADJOE'][0] + team_data.loc[
            team_data['TEAM'] == mm_games_19['Home Team'][i],
            ['ADJDE']].reset_index()['ADJDE'][0]
    mm_games_19['t2_points'][i] = team_data.loc[
        team_data['TEAM'] == mm_games_19['Home Team'][i],
        ['ADJOE']].reset_index()['ADJOE'][0] + team_data.loc[
            team_data['TEAM'] == mm_games_19['Away Team'][i],
            ['ADJDE']].reset_index()['ADJDE'][0]

all_games_19['pts_difference'] = all_games_19.t1_points - all_games_19.t2_points
mm_games_19['pts_difference'] = mm_games_19.t1_points - mm_games_19.t2_points

scaler = MinMaxScaler()
scaled_differences = scaler.fit_transform(all_games_19[['pts_difference']])
for i in range(len(all_games_19)):
    all_games_19['pts_difference'][i] = scaled_differences[i][0]

scaled_differences = scaler.fit_transform(mm_games_19[['pts_difference']])
for i in range(len(mm_games_19)):
    mm_games_19['pts_difference'][i] = scaled_differences[i][0]


with open('data/all_games_19_data.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow([
        'Away Team', 'Home Team', 'Winner', 't1_points', 't2_points',
        'Away Win', 'pts_difference'
    ])
    for i in range(len(all_games_19)):
        writer.writerow([
            all_games_19['Away Team'][i], all_games_19['Home Team'][i],
            all_games_19['Winner'][i], all_games_19['t1_points'][i],
            all_games_19['t2_points'][i], all_games_19['Away Win'][i],
            all_games_19['pts_difference'][i]
        ])

with open('data/mm_games_19_data.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow([
        'Away Team', 'Home Team', 'Winner', 't1_points', 't2_points', 'Away Win',
        'pts_difference'
    ])
    for i in range(len(mm_games_19)):
        writer.writerow([
            mm_games_19['Away Team'][i], mm_games_19['Home Team'][i],
            mm_games_19['Winner'][i], mm_games_19['t1_points'][i],
            mm_games_19['t2_points'][i], mm_games_19['Away Win'][i],
            all_games_19['pts_difference'][i]
        ])
