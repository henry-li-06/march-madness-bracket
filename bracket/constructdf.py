import pandas as pd
import numpy as np
import csv

all_games_19 = pd.read_csv('all_games_19.csv')
mm_games_19 = pd.read_csv('mm_games_19.csv')
team_data = pd.read_csv('cbb19.csv') 

all_games_19['ADJOE Difference'] = 0.0
all_games_19['ADJDE Difference'] = 0.0
all_games_19['ADJ_T Difference'] = 0.0
all_games_19['TOR Difference'] = 0.0
all_games_19['EFG_O Difference'] = 0.0
all_games_19['ORB Difference'] = 0.0
all_games_19['DRB Difference'] = 0.0
all_games_19['FTR Difference'] = 0.0
all_games_19['Away Win'] = 'N'

mm_games_19['ADJOE Difference'] = 0.0
mm_games_19['ADJDE Difference'] = 0.0
mm_games_19['ADJ_T Difference'] = 0.0
mm_games_19['TOR Difference'] = 0.0
mm_games_19['EFG_O Difference'] = 0.0
mm_games_19['ORB Difference'] = 0.0
mm_games_19['DRB Difference'] = 0.0
mm_games_19['FTR Difference'] = 0.0
mm_games_19['Away Win'] = 'N'

# all_games_19 calculating ADJOE, ADJDE, TOR, and ADJ_T
for i in range(len(all_games_19)):
    print(i)
    if(all_games_19['Away Team'][i] == all_games_19['Winner'][i]):
        all_games_19['Away Win'][i] = 'Y'
    all_games_19['ADJOE Difference'][i] = team_data.loc[team_data['TEAM'] == all_games_19['Away Team'][i], \
        ['ADJOE']].reset_index()['ADJOE'][0] - team_data.loc[team_data['TEAM'] == all_games_19['Home Team'][i], \
            ['ADJOE']].reset_index()['ADJOE'][0]
    all_games_19['ADJDE Difference'][i] = team_data.loc[team_data['TEAM'] == all_games_19['Away Team'][i], \
        ['ADJDE']].reset_index()['ADJDE'][0] - team_data.loc[team_data['TEAM'] == all_games_19['Home Team'][i], \
            ['ADJDE']].reset_index()['ADJDE'][0] 
    all_games_19['ADJ_T Difference'][i] = team_data.loc[team_data['TEAM'] == all_games_19['Away Team'][i], \
        ['ADJ_T']].reset_index()['ADJ_T'][0] - team_data.loc[team_data['TEAM'] == all_games_19['Home Team'][i], \
            ['ADJ_T']].reset_index()['ADJ_T'][0] 
    all_games_19['TOR Difference'][i] = team_data.loc[team_data['TEAM'] == all_games_19['Away Team'][i], \
        ['TOR']].reset_index()['TOR'][0] - team_data.loc[team_data['TEAM'] == all_games_19['Home Team'][i], \
            ['TOR']].reset_index()['TOR'][0] 

# mm_games_19 calculating ADJOE, ADJDE, TOR, and ADJ_T
for i in range(len(mm_games_19)):
    if(mm_games_19['Away Team'][i] == mm_games_19['Winner'][i]):
        mm_games_19['Away Win'][i] = 'Y'
    mm_games_19['ADJOE Difference'][i] = team_data.loc[team_data['TEAM'] == mm_games_19['Away Team'][i], \
        ['ADJOE']].reset_index()['ADJOE'][0] - team_data.loc[team_data['TEAM'] == mm_games_19['Home Team'][i], \
            ['ADJOE']].reset_index()['ADJOE'][0]
    mm_games_19['ADJDE Difference'][i] = team_data.loc[team_data['TEAM'] == mm_games_19['Away Team'][i], \
        ['ADJDE']].reset_index()['ADJDE'][0] - team_data.loc[team_data['TEAM'] == mm_games_19['Home Team'][i], \
            ['ADJDE']].reset_index()['ADJDE'][0] 
    mm_games_19['ADJ_T Difference'][i] = team_data.loc[team_data['TEAM'] == mm_games_19['Away Team'][i], \
        ['ADJ_T']].reset_index()['ADJ_T'][0] - team_data.loc[team_data['TEAM'] == mm_games_19['Home Team'][i], \
            ['ADJ_T']].reset_index()['ADJ_T'][0] 
    mm_games_19['TOR Difference'][i] = team_data.loc[team_data['TEAM'] == mm_games_19['Away Team'][i], \
        ['TOR']].reset_index()['TOR'][0] - team_data.loc[team_data['TEAM'] == mm_games_19['Home Team'][i], \
            ['TOR']].reset_index()['TOR'][0]

# all_games_19 calculating EFG_O, TOR, ORB, and FTR
for i in range(len(all_games_19)):
    print(i)
    if(all_games_19['Away Team'][i] == all_games_19['Winner'][i]):
        all_games_19['Away Win'][i] = 'Y'
    all_games_19['EFG_O Difference'][i] = team_data.loc[team_data['TEAM'] == all_games_19['Away Team'][i], \
        ['EFG_O']].reset_index()['EFG_O'][0] - team_data.loc[team_data['TEAM'] == all_games_19['Home Team'][i], \
            ['EFG_O']].reset_index()['EFG_O'][0]
    all_games_19['TOR Difference'][i] = team_data.loc[team_data['TEAM'] == all_games_19['Away Team'][i], \
        ['TOR']].reset_index()['TOR'][0] - team_data.loc[team_data['TEAM'] == all_games_19['Home Team'][i], \
            ['TOR']].reset_index()['TOR'][0] 
    all_games_19['ORB Difference'][i] = team_data.loc[team_data['TEAM'] == all_games_19['Away Team'][i], \
        ['ORB']].reset_index()['ORB'][0] - team_data.loc[team_data['TEAM'] == all_games_19['Home Team'][i], \
            ['ORB']].reset_index()['ORB'][0] 
    all_games_19['DRB Difference'][i] = team_data.loc[team_data['TEAM'] == all_games_19['Away Team'][i], \
        ['DRB']].reset_index()['DRB'][0] - team_data.loc[team_data['TEAM'] == all_games_19['Home Team'][i], \
            ['DRB']].reset_index()['DRB'][0] 
    all_games_19['FTR Difference'][i] = team_data.loc[team_data['TEAM'] == all_games_19['Away Team'][i], \
        ['TOR']].reset_index()['TOR'][0] - team_data.loc[team_data['TEAM'] == all_games_19['Home Team'][i], \
            ['TOR']].reset_index()['TOR'][0] 

# mm_games_19 calculating EFG_O, TOR, ORB, and FTR
for i in range(len(mm_games_19)):
    if(mm_games_19['Away Team'][i] == mm_games_19['Winner'][i]):
        mm_games_19['Away Win'][i] = 'Y'
    mm_games_19['EFG_O Difference'][i] = team_data.loc[team_data['TEAM'] == mm_games_19['Away Team'][i], ['EFG_O']].reset_index()['EFG_O'][0] - team_data.loc[team_data['TEAM'] == mm_games_19['Home Team'][i], ['EFG_O']].reset_index()['EFG_O'][0]
    mm_games_19['TOR Difference'][i] = team_data.loc[team_data['TEAM'] == mm_games_19['Away Team'][i], \
        ['TOR']].reset_index()['TOR'][0] - team_data.loc[team_data['TEAM'] == mm_games_19['Home Team'][i], \
            ['TOR']].reset_index()['TOR'][0] 
    mm_games_19['ORB Difference'][i] = team_data.loc[team_data['TEAM'] == mm_games_19['Away Team'][i], \
        ['ORB']].reset_index()['ORB'][0] - team_data.loc[team_data['TEAM'] == mm_games_19['Home Team'][i], \
            ['ORB']].reset_index()['ORB'][0] 
    mm_games_19['DRB Difference'][i] = team_data.loc[team_data['TEAM'] == mm_games_19['Away Team'][i], \
        ['DRB']].reset_index()['DRB'][0] - team_data.loc[team_data['TEAM'] == mm_games_19['Home Team'][i], \
            ['DRB']].reset_index()['DRB'][0] 
    mm_games_19['FTR Difference'][i] = team_data.loc[team_data['TEAM'] == mm_games_19['Away Team'][i], \
        ['FTR']].reset_index()['FTR'][0] - team_data.loc[team_data['TEAM'] == mm_games_19['Home Team'][i], \
            ['FTR']].reset_index()['FTR'][0]

# basically want to write the dataframe into a csv file because otherwise it takes too long
with open('all_games_19_data.csv', 'w', newline = '') as csvfile:
    writer = csv.writer(csvfile, delimiter = ',')
    writer.writerow(['Away Team', 'Home Team', 'Winner', 'ADJOE Difference', 'ADJDE Difference', \
        'ADJ_T Difference', 'TOR Difference', 'EFG_O Difference', 'ORB Difference', 'DRB Difference', \
            'FTR Difference', 'Away Win'])
    for i in range(len(all_games_19)):
        writer.writerow([all_games_19['Away Team'][i], all_games_19['Home Team'][i], \
            all_games_19['Winner'][i], all_games_19['ADJOE Difference'][i], \
                all_games_19['ADJDE Difference'][i], all_games_19['ADJ_T Difference'][i], \
                    all_games_19['TOR Difference'][i], all_games_19['EFG_O Difference'][i], \
                        all_games_19['ORB Difference'][i], all_games_19['DRB Difference'][i], \
                            all_games_19['FTR Difference'][i], all_games_19['Away Win'][i]])

with open('mm_games_19_data.csv', 'w', newline = '') as csvfile:
    writer = csv.writer(csvfile, delimiter = ',')
    writer.writerow(['Away Team', 'Home Team', 'Winner', 'ADJOE Difference', 'ADJDE Difference', \
        'ADJ_T Difference', 'TOR Difference', 'EFG_O Difference', 'ORB Difference', 'DRB Difference', \
            'FTR Difference', 'Away Win'])    
    for i in range(len(mm_games_19)):
        writer.writerow([mm_games_19['Away Team'][i], mm_games_19['Home Team'][i], \
            mm_games_19['Winner'][i], mm_games_19['ADJOE Difference'][i], \
                mm_games_19['ADJDE Difference'][i], mm_games_19['ADJ_T Difference'][i], \
                    mm_games_19['TOR Difference'][i], mm_games_19['EFG_O Difference'][i], \
                        mm_games_19['ORB Difference'][i], mm_games_19['DRB Difference'][i], \
                            mm_games_19['FTR Difference'][i], mm_games_19['Away Win'][i]])
