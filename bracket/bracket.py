from model import model, all_games_19
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
import pandas as pd


class Node:
    '''
    Data should be "N/A" if the winner hasn't been predicted yet
    '''
    # vertical separation between nodes
    VERTICAL_SEPARATION = [0, 0, 150, 65, 30, 15, 8]
    # horizontal separation between nodes
    HORIZONTAL_SEPARATION = 80

    data = pd.read_csv('bracket/data/all_games_19_data.csv', index_col=0).drop(
        columns=['Away Team', 'Home Team', 'Winner', 'Away Win'])
    scaler = MinMaxScaler()
    pca = PCA(n_components=8)
    pca.fit(scaler.fit_transform(data))

    seeds = [1, 8, 5, 4, 6, 3, 7, 2]
    regions = ['East', 'South', 'West', 'Midwest']

    i = 0  # iterator for adding teams

    @classmethod
    def init_data(cls, year):
        cls.team_data = pd.read_csv('bracket/data/cbb{}.csv'.format(year))
        cls.features = list(
            cls.team_data.drop(
                columns=['TEAM', 'CONF', 'G', 'W', 'POSTSEASON', 'SEED', 'REGION'
                         ]).columns)
        cls.first_round_games = []
        for region in cls.regions:
            for seed in cls.seeds:
                game = []
                team1 = cls.team_data.loc[(cls.team_data['SEED'] == seed) &
                                          (cls.team_data['REGION'] == region),
                                          'TEAM'].reset_index()['TEAM'][0]
                team2 = cls.team_data.loc[(cls.team_data['SEED'] == 17 - seed) & (
                    cls.team_data['REGION'] == region)].reset_index()['TEAM'][0]
                game.append(team1)
                game.append(team2)
                cls.first_round_games.append(game)

    def __init__(self, data, d, x, y):
        self.data = data
        self.left = None
        self.right = None
        self.depth = d
        self.x = x
        self.y = y

    def __str__(self):
        return self.data

    def insert(self, data):
        if (self.left is None):
            self.left = Node(data, self.depth + 1)
        elif (self.right is None):
            self.right = Node(data, self.depth + 1)
        else:
            return "Cannot insert node."

    def print_tree(self):
        if (not self.left is None):
            self.left.print_tree()
        # print(self.data)
        if (not self.right is None):
            self.right.print_tree()

    def create_tree(self):
        self.left = Node('N/A', self.depth + 1,
                         self.x - Node.HORIZONTAL_SEPARATION, self.y)
        self.right = Node('N/A', self.depth + 1,
                          self.x + Node.HORIZONTAL_SEPARATION, self.y)
        self.left.create_tree_left()
        self.right.create_tree_right()

    def create_tree_left(self):
        if (self.depth < 5):
            self.left = Node('N/A', self.depth + 1,
                             self.x - Node.HORIZONTAL_SEPARATION,
                             self.y + Node.VERTICAL_SEPARATION[self.depth + 1])
            self.right = Node(
                'N/A', self.depth + 1, self.x - Node.HORIZONTAL_SEPARATION,
                self.y - Node.VERTICAL_SEPARATION[self.depth + 1])
            self.left.create_tree_left()
            self.right.create_tree_left()

    def create_tree_right(self):
        if (self.depth < 5):
            self.left = Node('N/A', self.depth + 1,
                             self.x + Node.HORIZONTAL_SEPARATION,
                             self.y - Node.VERTICAL_SEPARATION[self.depth + 1])
            self.right = Node(
                'N/A', self.depth + 1, self.x + Node.HORIZONTAL_SEPARATION,
                self.y + Node.VERTICAL_SEPARATION[self.depth + 1])
            self.left.create_tree_right()
            self.right.create_tree_right()

    def add_teams(self):
        self.left.add_teams_left()
        self.right.add_teams_right()

    def add_teams_left(self):
        if (self.depth == 5):
            self.left = Node(self.first_round_games[Node.i][0], self.depth + 1,
                             self.x - Node.HORIZONTAL_SEPARATION,
                             self.y + Node.VERTICAL_SEPARATION[self.depth + 1])
            self.right = Node(
                self.first_round_games[Node.i][1], self.depth + 1,
                self.x - Node.HORIZONTAL_SEPARATION,
                self.y - Node.VERTICAL_SEPARATION[self.depth + 1])
            Node.i += 1
        else:
            self.left.add_teams_left()
            self.right.add_teams_left()

    def add_teams_right(self):
        if (self.depth == 5):
            self.left = Node(self.first_round_games[Node.i][0], self.depth + 1,
                             self.x + Node.HORIZONTAL_SEPARATION,
                             self.y - Node.VERTICAL_SEPARATION[self.depth + 1])
            self.right = Node(
                self.first_round_games[Node.i][1], self.depth + 1,
                self.x + Node.HORIZONTAL_SEPARATION,
                self.y + Node.VERTICAL_SEPARATION[self.depth + 1])
            Node.i += 1
        else:
            self.left.add_teams_right()
            self.right.add_teams_right()

    def build_tree(self):
        self.create_tree()
        self.add_teams()

    def check_tree(self):
        if (self.depth == 5):
            print(self)
        else:
            self.left.check_tree()
            self.right.check_tree()

    def make_prediction(self):
        if (self.left.data != 'N/A'):
            self.data = Node.make_game_prediction(self.left.data,
                                                  self.right.data)
        else:
            self.left.make_predictions()
            self.right.make_predictions()

    def make_predictions(self):
        while (self.data == 'N/A'):
            self.make_prediction()

    @classmethod
    def make_game_prediction(cls, away_team, home_team):
        inputs = []
        for feature in cls.features:
            away_team_val = cls.team_data.loc[
                cls.team_data['TEAM'] == away_team,
                [feature]].reset_index()[feature][0]
            home_team_val = cls.team_data.loc[
                cls.team_data['TEAM'] == home_team,
                [feature]].reset_index()[feature][0]
            inputs.append(away_team_val - home_team_val)

        scaled_features = cls.scaler.transform([inputs])
        pca_projection = cls.pca.transform(scaled_features)
        prediction = model.predict(pca_projection)
        return away_team if prediction[0] == 'Y' else home_team
