
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

all_games_19 = pd.read_csv('bracket/data/all_games_19_data.csv')
team_data = pd.read_csv('bracket/data/cbb19.csv')

features = all_games_19[['pts_difference']]
target = all_games_19['Away Win']

x_train, x_test, y_train, y_test = train_test_split(features, target, test_size = 0.69)

model = SVC(kernel = 'linear')
model.fit(x_train, y_train)

