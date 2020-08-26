
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC, LinearSVC
from sklearn.linear_model import Perceptron
from sklearn.neighbors import KNeighborsClassifier

all_games_19 = pd.read_csv('bracket/data/all_games_19_data.csv')
team_data = pd.read_csv('bracket/data/cbb17.csv')

columns = []
for i in range(8):
    columns.append(str(i))

features = all_games_19[columns]
target = all_games_19['Away Win']

x_train, x_test, y_train, y_test = train_test_split(features, target, test_size = 0.3)
# model = LinearSVC(C = 150)
# model = SVC(C = 100)
model = KNeighborsClassifier(n_neighbors = 50)
# model = Perceptron()
model.fit(x_train, y_train)
