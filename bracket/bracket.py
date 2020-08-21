from model import model, team_data, all_games_19
from sklearn.preprocessing import StandardScaler, MinMaxScaler

class Node:
    '''
    Data should be "N/A" if the winner hasn't been predicted yet
    '''

    VERTICAL_SEPARATION = [0, 0, 150, 65, 30, 15, 8] # vertical separation between nodes
    HORIZONTAL_SEPARATION = 80 # horizontal separation between nodes 
    #VERTICAL_DECREASE = 8 # vertical increase as depth of nodes increas
    
    i = 0 # iterator for adding teams

    scaler = MinMaxScaler()
    scaler.fit(all_games_19[['pts_difference']])

    features = ['ADJOE' ,'ADJDE', '3P_O', 'EFG_O', 'ORB', 'FTR']

    first_round_games = [] # 2D array of first round games 
    seeds = [1, 8, 5, 4, 6, 3, 7, 2]
    regions = ['East', 'South', 'West', 'Midwest']
    for region in regions:
        for seed in seeds:
            game = []
            team1 = team_data.loc[(team_data['SEED'] == seed) & (team_data['REGION'] == region), 'TEAM'].reset_index()['TEAM'][0]
            team2 = team_data.loc[(team_data['SEED'] == 17 - seed) & (team_data['REGION'] == region)].reset_index()['TEAM'][0]
            game.append(team1)
            game.append(team2)
            first_round_games.append(game)
    
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
        if(self.left is None):
            self.left = Node(data, self.depth + 1)
        elif(self.right is None):
            self.right = Node(data, self.depth + 1)
        else:
            return "Cannot insert node."
       
    def print_tree(self):
        if(not self.left is None):
            self.left.print_tree()
        #print(self.data)
        if(not self.right is None):
            self.right.print_tree()
    
    def create_tree(self):
        self.left = Node('N/A', self.depth + 1, self.x - Node.HORIZONTAL_SEPARATION, self.y)
        self.right = Node('N/A', self.depth + 1, self.x + Node.HORIZONTAL_SEPARATION, self.y)
        self.left.create_tree_left()
        self.right.create_tree_right()

    def create_tree_left(self):
        if(self.depth < 5):
            self.left = Node('N/A', self.depth + 1, self.x - Node.HORIZONTAL_SEPARATION, self.y + \
                Node.VERTICAL_SEPARATION[self.depth + 1])
            self.right = Node('N/A', self.depth + 1, self.x - Node.HORIZONTAL_SEPARATION, self.y - \
                Node.VERTICAL_SEPARATION[self.depth + 1])
            self.left.create_tree_left()
            self.right.create_tree_left()
    
    def create_tree_right(self):
        if(self.depth < 5):
            self.left = Node('N/A', self.depth + 1, self.x + Node.HORIZONTAL_SEPARATION, self.y - \
                Node.VERTICAL_SEPARATION[self.depth + 1])
            self.right = Node('N/A', self.depth + 1, self.x + Node.HORIZONTAL_SEPARATION, self.y + \
                Node.VERTICAL_SEPARATION[self.depth + 1])
            self.left.create_tree_right()
            self.right.create_tree_right()

    def add_teams(self):
        self.left.add_teams_left()
        self.right.add_teams_right()

    def add_teams_left(self):
        if(self.depth == 5):
            #print(Node.i)
            #print(self.first_round_games[Node.i][0] + ' ' + self.first_round_games[Node.i][1])
            self.left = Node(self.first_round_games[Node.i][0], self.depth + 1, self.x - \
                Node.HORIZONTAL_SEPARATION, self.y + Node.VERTICAL_SEPARATION[self.depth + 1])
            self.right = Node(self.first_round_games[Node.i][1], self.depth + 1, self.x - \
                Node.HORIZONTAL_SEPARATION, self.y - Node.VERTICAL_SEPARATION[self.depth + 1])
            Node.i += 1
        else:
            self.left.add_teams_left()
            self.right.add_teams_left()
    
    def add_teams_right(self):
        if(self.depth == 5):
            #print(Node.i)
            #print(self.first_round_games[Node.i][0] + ' ' + self.first_round_games[Node.i][1])
            self.left = Node(self.first_round_games[Node.i][0], self.depth + 1, self.x + \
                Node.HORIZONTAL_SEPARATION, self.y - Node.VERTICAL_SEPARATION[self.depth + 1])
            self.right = Node(self.first_round_games[Node.i][1], self.depth + 1, self.x + \
                Node.HORIZONTAL_SEPARATION, self.y + Node.VERTICAL_SEPARATION[self.depth + 1])
            Node.i += 1
        else:
            self.left.add_teams_right()
            self.right.add_teams_right()
    
    def build_tree(self):
        self.create_tree()
        self.add_teams()
    
    def check_tree(self):
        if(self.depth == 5):
            print(self)
        else:
            self.left.check_tree()
            self.right.check_tree()
    
    def make_prediction(self):
        if(self.left.data != 'N/A'):
            #print(make_prediction(self.left.data, self.right.data))
            self.data = Node.make_game_prediction(self.left.data, self.right.data)
        else:
            self.left.make_predictions()
            self.right.make_predictions()
    
    def make_predictions(self):
        while(self.data == 'N/A'):
            self.make_prediction()

    
    # @staticmethod
    # def make_game_prediction(team1, team2):
    #     t1_points = team_data.loc[team_data['TEAM'] == team1, ['ADJOE']].reset_index()['ADJOE'][0] \
    #         + team_data.loc[team_data['TEAM'] == team2, ['ADJDE']].reset_index()['ADJDE'][0]
    #     t2_points = team_data.loc[team_data['TEAM'] == team2, ['ADJOE']].reset_index()['ADJOE'][0] \
    #         + team_data.loc[team_data['TEAM'] == team1, ['ADJDE']].reset_index()['ADJDE'][0]

    #     return team1 if t1_points > t2_points else team2
    @classmethod
    def make_game_prediction(cls, team1, team2):
        inputs = []
        inputs.append(team_data.loc[team_data['TEAM'] == team1, ['ADJOE']].reset_index()['ADJOE'][0] \
            + team_data.loc[team_data['TEAM'] == team2, ['ADJDE']].reset_index()['ADJDE'][0])
        inputs.append(team_data.loc[team_data['TEAM'] == team2, ['ADJOE']].reset_index()['ADJOE'][0] \
            + team_data.loc[team_data['TEAM'] == team1, ['ADJDE']].reset_index()['ADJDE'][0])
        game = []
        game.append([inputs[0] - inputs[1]])
        scaled_data = cls.scaler.transform(game)
        prediction = model.predict(scaled_data)
        print(prediction[0])
        return team1 if prediction[0] == 'Y' else team2
        


def make_prediction(team1, team2, features):
    inputs = []
    for feature in features:
        val = team_data.loc[team_data['TEAM'] == team1, [feature]].reset_index()[feature][0] \
        - team_data.loc[team_data['TEAM'] == team2, \
            [feature]].reset_index()[feature][0]
        inputs.append(val)
    game = []
    game.append(inputs)
    prediction = model.predict(game)
    print(prediciton[0])
    if(prediction[0] == 'Y'):
        return team1
    else:
        return team2

def make_prediction1(team1, team2, features):
    #if(not(team1 in teams and team2 in teams)):
    #    return 'Please enter valid teams'
    # Need to get the differences and store them in lists    
    inputs = [] # Need to make this into some 2D array kind of thing 
    ADJOE_difference = team_data.loc[team_data['TEAM'] == team1, ['ADJOE']].reset_index()['ADJOE'][0] \
        - team_data.loc[team_data['TEAM'] == team2, \
            ['ADJOE']].reset_index()['ADJOE'][0]
    ADJDE_difference = team_data.loc[team_data['TEAM'] == team1, \
        ['ADJDE']].reset_index()['ADJDE'][0] - team_data.loc[team_data['TEAM'] == team2, \
            ['ADJDE']].reset_index()['ADJDE'][0]
    # ADJ_T_difference = team_data.loc[team_data['TEAM'] == team1, \
    #    ['ADJ_T']].reset_index()['ADJ_T'][0] - team_data.loc[team_data['TEAM'] == team2, \
    #        ['ADJ_T']].reset_index()['ADJ_T'][0]
    # EFG_O_difference = team_data.loc[team_data['TEAM'] == team1, \
    #    ['EFG_O']].reset_index()['EFG_O'][0] - team_data.loc[team_data['TEAM'] == team2, \
    #        ['EFG_O']].reset_index()['EFG_O'][0] 
    # TOR_difference = team_data.loc[team_data['TEAM'] == team1, \
    #    ['TOR']].reset_index()['TOR'][0] - team_data.loc[team_data['TEAM'] == team2, \
    #        ['TOR']].reset_index()['TOR'][0]
    ORB_difference = team_data.loc[team_data['TEAM'] == team1, \
        ['ORB']].reset_index()['ORB'][0] - team_data.loc[team_data['TEAM'] == team2, \
            ['ORB']].reset_index()['ORB'][0]
    # DRB_difference = team_data.loc[team_data['TEAM'] == team1, \
    #    ['DRB']].reset_index()['DRB'][0] - team_data.loc[team_data['TEAM'] == team2, \
    #        ['DRB']].reset_index()['DRB'][0]
    FTR_difference = team_data.loc[team_data['TEAM'] == team1, \
        ['FTR']].reset_index()['FTR'][0] - team_data.loc[team_data['TEAM'] == team2, \
            ['FTR']].reset_index()['FTR'][0]
    
    features.append(ADJOE_difference)
    features.append(ADJDE_difference)
    features.append(ORB_difference)
    #features.append(ADJ_T_difference)
    #features.append(EFG_O_difference)
    #features.append(TOR_difference)
    #features.append(DRB_difference)
    features.append(FTR_difference)
    
    game = []
    game.append(features)
    prediction = model.predict(game)
    print(prediction[0])
    if(prediction[0] == 'Y'):
        return team1
    else:
        return team2
            