import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA

all_games_19 = pd.read_csv('data/all_games_19.csv')
mm_games_19 = pd.read_csv('data/mm_games_19.csv')
team_data = pd.read_csv('data/cbb19.csv')

all_games_19['Away Win'] = 'N'
for i in range(len(all_games_19)):
    if (all_games_19['Away Team'][i] == all_games_19['Winner'][i]):
        all_games_19['Away Win'][i] = 'Y'

features = list(
    team_data.drop(
        columns=['TEAM', 'CONF', 'G', 'W', 'POSTSEASON', 'SEED', 'REGION'
                 ]).columns)

for feature in features:
    column_name = feature + '_diff'
    all_games_19[column_name] = 0.0
    for i in range(len(all_games_19)):
        all_games_19[column_name][i] = team_data.loc[
            team_data['TEAM'] == all_games_19['Away Team'][i],
            [feature]].reset_index()[feature][0] - team_data.loc[
                team_data['TEAM'] == all_games_19['Home Team'][i],
                [feature]].reset_index()[feature][0]

all_games_19.to_csv('data/all_games_19_data.csv')

for i in range(len(features)):
    features[i] += '_diff'

scaler = MinMaxScaler()
scaled_features = scaler.fit_transform(all_games_19[features])

for i in range(len(features)):
    all_games_19[features[i]] = scaled_features[:, i]

pca = PCA(n_components=8)
pca_projection = pca.fit_transform(all_games_19[features])
df = pd.DataFrame(pca_projection)
all_games_19 = pd.concat([all_games_19, df], axis=1)
all_games_19.drop(columns=features, inplace=True)

all_games_19.to_csv('data/all_games_19_training_data.csv')
