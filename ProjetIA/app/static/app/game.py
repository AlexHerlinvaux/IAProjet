import itertools
from copy import deepcopy
from random import randint
import random
import csv

size_matrix = 8

#############################################################
class Board:
    def __init__(self) :
        self._cases = [[0 for col in range(0,size_matrix)] for row in range(0,size_matrix)]
        
    @property
    def cases(self) :
        return self._cases
    
    def set_case(self, pos, player_value) :
        x,y = pos
        self.cases[x][y] = player_value
        
    def get_pos(self, pos_x, pos_y): #return who's claimed the cell
        return self.cases[pos_x][pos_y]

    def fill_cases_tmp(self, init_pos, cases_tmp, player_value) :
        x, y = init_pos
        
        if x - 1 >= 0 and cases_tmp[x-1][y] != player_value :
                cases_tmp[x-1][y] = player_value
                cases_tmp = self.fill_cases_tmp((x-1,y), cases_tmp, player_value)
        if x + 1 < size_matrix and cases_tmp[x+1][y] != player_value :
                cases_tmp[x+1][y] = player_value
                cases_tmp = self.fill_cases_tmp((x+1,y), cases_tmp, player_value)
        if y - 1 >= 0 and cases_tmp[x][y-1] != player_value :
                cases_tmp[x][y-1] = player_value
                cases_tmp = self.fill_cases_tmp((x,y-1), cases_tmp, player_value)
        if y + 1 < size_matrix and cases_tmp[x][y+1] != player_value :
                cases_tmp[x][y+1] = player_value
                cases_tmp = self.fill_cases_tmp((x,y+1), cases_tmp, player_value)
            
        return cases_tmp
    
    def shape_detection(self, pos, player_value):
        cases_tmp = deepcopy(self.cases)
        
        if player_value == -1 :
            cases_tmp = self.fill_cases_tmp((size_matrix-1,size_matrix-1),cases_tmp, player_value)
        else :
            cases_tmp = self.fill_cases_tmp((0,0),cases_tmp, player_value)
        
        nb_cases_fill = 0
        for i in range(size_matrix):
            for j in range(size_matrix):
                if cases_tmp[i][j] == 0:
                    self.set_case((i,j),player_value)
                    nb_cases_fill += 1
        return nb_cases_fill
            
    
    def draw_cell(self, pos, player_value) :
        self.set_case(pos, player_value)
        self.shape_detection(pos, player_value)
        
    
    def restart(self):
        self._cases = [[0 for col in range(0,size_matrix)] for row in range(0,size_matrix)]
    
            
        
#############################################################
       
   
     
#############################################################     
class User:
    def __init__(self, name, password) :
        self._name = name
        self._pasword = password
        self._nb_games_played = 0
        self._nb_games_won = 0


    @property
    def name(self):
        return self._name   
    
    
    @name.setter
    def name(self, name):
        self._name = name
    
#############################################################
    


#############################################################
class Player (User):
    def __init__(self, name, password, is_human = True, trainable = False) :
        User.__init__(self,name, password)
        self._position = []
        self._game = None
        
        self.is_human = is_human
        self.trainable = trainable
        self.histo_trans = []
        #self.V = [[0 for col in range(0,size_matrix)] for row in range(0,size_matrix)]
        self.Q = dict()
        self.rewards = []
        self.eps = 0.99 if trainable else 0.05
        self.learning_rate = 0.01
        self.discount_rate = 0.01
        self._last_state = None
        self._last_action = None
        self.points = 0
    
    @property
    def position(self):
        return self._position
    
    
    @position.setter
    def position(self,pos):
        self._position = pos
         
        
    @property
    def game(self):
        return self._game
    
    @property
    def last_state(self):
        return self._last_state
    
    @last_state.setter
    def last_state(self, last_state):
        self._last_state = last_state
    
    @property
    def last_action(self):
        return self._last_action
    
    @last_action.setter
    def last_action(self, last_action):
        self._last_action = last_action
        
    @game.setter
    def game(self, new_game):
        self._game = new_game
        
    def init_Q(self, state):
        self.Q[str(state)] = [0,0,0,0]
        
    def get_Q(self):
        return self.Q
        
    def save_histo(self, direction,  pos_X, pos_Y):
        if direction == 1:
            self.position = (pos_X, pos_Y-1)
            self.game.histo_pos = (pos_X, pos_Y-1)
        elif direction == 2:
            self.position = (pos_X, pos_Y+1)
            self.game.histo_pos = (pos_X, pos_Y+1)
        elif direction == 3:
            self.position = (pos_X-1, pos_Y)
            self.game.histo_pos = (pos_X-1, pos_Y)
        else:
            self.position = (pos_X+1, pos_Y)
            self.game.histo_pos = (pos_X+1, pos_Y)
        
    def convert_action_into_offset(self, direction):
        if direction == 1:      #go left
            X_offset = 0
            Y_offset = -1
        elif direction == 2:    #go right
            X_offset = 0
            Y_offset = 1
        elif direction == 3:    #go up
            X_offset = -1
            Y_offset = 0
        else :                  #go down
            X_offset = 1
            Y_offset = 0
        
        return X_offset, Y_offset
    
    def check_move(self, direction):
        pos_X, pos_Y = self.position
        X_offset, Y_offset = self.convert_action_into_offset(direction)
        
            #check if position is in array's boundaries
        if((pos_X+X_offset >= 0 and pos_X+X_offset <= size_matrix-1) and
           (pos_Y+Y_offset >= 0 and pos_Y+Y_offset <= size_matrix-1)):
                    #check if the cell is already claimed
            return (self.game.board().get_pos(pos_X+X_offset ,pos_Y+Y_offset) == 0 or
                    self.game.board().get_pos(pos_X+X_offset ,pos_Y+Y_offset) == self.game.turn)
        return False
    
    
    def move(self, direction):
        pos_X, pos_Y = self.position
        
        if(self.check_move(direction)) :
            self.save_histo(direction, pos_X, pos_Y)
            self.game.board().draw_cell(self.position, self.game.turn)
        
    
    def Reward(self, state):
        cases, *_ = state

        p1_points  = 0
        p2_points  = 0
        for ligne in cases:
            p1_points += ligne.count(-1)
            p2_points += ligne.count(1)

        p1_points -= self.points
        p2_points -= self.game._p2.points
        return p1_points - p2_points
 
    def Q_fct(self, state, points):
        
        if self.last_state is not None:
            if str(state) not in self.Q.keys():
                self.Q[str(state)] = [0,0,0,0]
            
            if str(self.last_state) not in self.Q.keys():
                self.Q[str(self.last_state)] = [0,0,0,0]
                
            if self.check_move(self.last_action) :            
                max_prime = max(self.Q[str(state)])
                # new Q = Q actuel + learning rate * (reward + discount rate * (max Q suivant - Q actuel))
                self.Q[str(self.last_state)][self.last_action-1] += self.learning_rate * (self.Reward(state) + 
                      self.discount_rate * (max_prime - self.Q[str(self.last_state)][self.last_action-1]))            
                
            else:
                self.Q[str(self.last_state)][self.last_action-1] = -100000000
        
        self._last_state = deepcopy(state)
    
    def action(self):
        pl = self.name + " >"
        action = int(input(pl))
        self.move(action)
    
    
    def action_bot(self, state) :
        if self.trainable :
            cases, _ , turn_player = state
            points = cases.count(turn_player)
            if(random.uniform(0,1) < self.eps) :
                action = randint(1,4)
                
                if self.last_action is None:
                    self.last_action = action
                self.Q_fct(state, points)
                self.move(action)
                self.last_action = action
            else :
                if str(state) not in self.Q.keys():
                    self.Q[str(state)] = [0,0,0,0]
                max_value = max(self.Q[str(state)])
                max_move = self.Q[str(state)].index(max_value)
                self.move(max_move + 1)
        else:
            action = randint(1,4)
            self.move(action)
           
           
        
    
    
        
    #value function            
    """            
    def greedy_step(self):
        # Greedy step
        actions = [(0,-1), (0,1), (-1,0), (1,0)]
        state, *rest = self.histo_trans[-1]
        pos_X, pos_Y = self.position
        vmin = None
        vi = None
        for i in range(0, 4):
            ax,ay = actions[i]
            if self.check_move(i) and self.game.state != "Over" and 
                (vmin is None or vmin > self.V[pos_X+ax][pos_Y+ay]):
                vmin = self.V[pos_X+ax][pos_Y+ay]
                vi = i
        return actions[vi]
    
    def add_transition(self, n_tuple):
        # Add one transition to the history: tuple (s, a , r, s')
        self.history.append(n_tuple)
        state, action, reward, n_state = n_tuple
        self.rewards.append(reward)
    
            
    def train(self):
        if not self.trainable or self.is_human:
            return
        
        # Update the value function if this player is not human
        actions = [(0,-1), (0,1), (-1,0), (1,0)] # possible actions
        histo_pos = reversed(self.game.histo_pos)
        i_histo_pos = 0
        for transition in reversed(self.histo_trans):
            state, action, reward, n_state = transition
            ax,ay = actions[action-1] # get action to next state
            i,j = histo_pos[i_histo_pos]
            if reward == 0:
                self.V[state[i][j]] += 0.00001*(self.V[n_state[i+ax][j+ay]] - self.V[state[i][j]])
            else:
                self.V[state[i][j]] += 0.00001*(reward - self.V[state[i][j]])
                    
        self.histo_trans = []
    """    
        
#############################################################
  


#############################################################
class Game :
    def __init__(self, player1, player2) :
        self._p1 = player1
        self._p2 = player2
        self._board = Board()
        self._players = [player1, player2]
        self._histo_pos = [[(0,0)],[(size_matrix-1,size_matrix-1)]]
        self._turn = [-1,1]
        self._players[0].game = self
        self._players[1].game = self
        self._state = "Not Started"
    
    
    @property
    def turn(self):
        return self._turn[0]
    
    def board(self):
        return self._board

    def player(self, i):
        return self._players[i]
    
    @property
    def state(self):
        return self._state
    
    @state.setter
    def state(self, new_state):
        self._state = new_state
    
    @property
    def histo_pos(self):
        return self._histo_pos
    
    @histo_pos.setter
    def histo_pos(self, pos):
        self._histo_pos[0].append(pos)

    def next_turn(self):
        self._turn.reverse()
        self._histo_pos.reverse()
        
    def starting(self):
        self.state = "Started"
        self._players[0].position = (0,0)
        self._players[1].position = (size_matrix-1,size_matrix-1)
        
        if not self._p1.is_human :
            with open("app/static/app/output_keys.csv", "r") as csvfile_keys:
                with open("app/static/app/output_vals.csv", "r") as csvfile_vals:
                    data_keys = csv.reader(csvfile_keys)
                    data_vals = csv.reader(csvfile_vals)
                    for key, val in zip(data_keys, data_vals):
                        self._p1.Q["".join(key)] = list(map(lambda x : float(x), val))
        
        self.board().set_case(self._players[0].position, self._turn[0])
        self.board().set_case(self._players[1].position, self._turn[1])
        #Draw board & players (Django)
        
    def restart(self):
        self._board = Board()
        self._players = [self._p1, self._p2]
        self._histo_pos = [[(0,0)],[(size_matrix-1,size_matrix-1)]]
        self._turn = [-1,1]
        self._players[0].game = self
        self._players[1].game = self
        self.starting()
    
    def check_state(self):
        if all(list(itertools.chain(*self.board().cases))):
            self.state = "Over"
            
    def check_winner(self):
        self._p1._nb_games_played += 1
        self._p2._nb_games_played += 1
        
        if self._p1.points > self._p2.points:
            self._p1._nb_games_won += 1
            return "player 1 won"
        else:
            self._p2._nb_games_won += 1
            return "player 2 won"
    
    def play(self, action_p1):
        for p in range(0,2):
            if self.state != "Over":
                state = self.board, self.player(p).position, self.turn
                if p == 1:
                    self.player(p).move(action_p1)
                else:
                    self.player(p).action_bot(state)
                self.next_turn()
                self.check_state()
        
    
            
    
#############################################################

#----------------------------
#           train IA
            
def train_IA():
    
    p1 = Player("p1", "pass1", is_human=False, trainable=True)
    p2 = Player("p2", "pass2", is_human=False)
    
    game = Game(p1, p2)
    game.starting()
    p1.init_Q((game.board().cases, p1.position, -1))
    win = 0
    for iPartie in range (0, 500):
        if iPartie% 10 == 0 and iPartie != 0 and game._p1.eps >= 0.3:
            game._p1.eps -= 0.01
        while game.state != "Over":
            for p in range(0,2):
                if game.state != "Over":
                    game.player(p).points = 0
                    for ligne in game.board().cases :
                        game.player(p).points += ligne.count(game.turn)
                    state = game.board().cases, game.player(p).position, game.turn
                    game.player(p).action_bot(state)
                    
                    game.next_turn()
                    game.check_state()
                    
        board_print = ""
        v1, v2= (0,0)
        for i in range(0,size_matrix):
            for j in range(0,size_matrix):
                board_print += str(game.board().get_pos(i,j)) + " "
                if game.board().get_pos(i,j) == 1 :
                    v1+=1
                else :
                    v2 += 1
            board_print += "\n"
        print(board_print)
        
        print(game.check_winner())
        
        if (v2 > v1) :
            win += 1
        
        game.restart()
        print(iPartie)
    
    print("winrate : " + str(win))
    with open("output_keys.csv", "w") as csvfile_keys:
        with open("output_vals.csv","w") as csvfile_vals:
            w1 = csv.writer(csvfile_keys)
            w2 = csv.writer(csvfile_vals)
            for key, val in p1.get_Q().items():
                w1.writerow([key])
                w2.writerow(val)
    

#-----------------------------
#           tests

#train_IA()


#---------------------------------
#              main

p1 = Player("p1","pass1",is_human=False, trainable=False)
p2 = Player("p2","pass2",is_human=True)

game = Game(p1, p2)
game.starting()
