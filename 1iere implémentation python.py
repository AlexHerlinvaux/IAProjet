
import itertools
from copy import deepcopy

#############################################################
class Board:
    def __init__(self) :
        self._cases = [[0 for col in range(0,8)] for row in range(0,8)]
        
        
    @property
    def cases(self) :
        return self._cases
    
    def set_case(self, pos, player_value) :
        x,y = pos
        self.cases[x][y] = player_value
    
    #return who's claimed the cell
    def get_pos(self, pos_x, pos_y):
        return self.cases[pos_x][pos_y]

    def fill_cases_tmp(self, init_pos, cases_tmp, player_value) :
        x, y = init_pos
                
        if x - 1 >= 0 and cases_tmp[x-1][y] != player_value :
                cases_tmp[x-1][y] = player_value
                cases_tmp = self.fill_cases_tmp((x-1,y), cases_tmp, player_value)
        if x + 1 < 8 and cases_tmp[x+1][y] != player_value :
                cases_tmp[x+1][y] = player_value
                cases_tmp = self.fill_cases_tmp((x+1,y), cases_tmp, player_value)
        if y - 1 >= 0 and cases_tmp[x][y-1] != player_value :
                cases_tmp[x][y-1] = player_value
                cases_tmp = self.fill_cases_tmp((x,y-1), cases_tmp, player_value)
        if y + 1 < 8 and cases_tmp[x][y+1] != player_value :
                cases_tmp[x][y+1] = player_value
                cases_tmp = self.fill_cases_tmp((x,y+1), cases_tmp, player_value)
            
        return cases_tmp
    
    def shape_detection(self, pos, player_value):
        cases_tmp = deepcopy(self.cases)
        if player_value == -1 :
            cases_tmp = self.fill_cases_tmp((7,7),cases_tmp, player_value)
        else :
            cases_tmp = self.fill_cases_tmp((0,0),cases_tmp, player_value)
        
        for i in range(8):
            for j in range(8):
                if cases_tmp[i][j] == 0:
                    self.set_case((i,j),player_value)
            
    
    def draw_cell(self, pos, player_value) :
        self.set_case(pos, player_value)
        self.shape_detection(pos, player_value)
        
    
        
    
            
        
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
    def __init__(self, name, password) :
        User.__init__(self,name, password)
        self._position = []
        self._game = None
        
        #self.is_human = is_human
        #self.trainable = trainable
    
    @property
    def position(self):
        return self._position
    
    
    @position.setter
    def position(self,pos):
        self._position = pos
         
        
    @property
    def game(self):
        return self._game
    
    @game.setter
    def game(self, new_game):
        self._game = new_game
        
        
    def check_move(self, direction):
        pos_X, pos_Y = self.position
        
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
            
            #check if position is in array's boundaries
        if((pos_X+X_offset >= 0 and pos_X+X_offset <= 7) and (pos_Y+Y_offset >=0 and pos_Y+Y_offset <= 7)):
                    #check if the cell is already claimed
            return (self.game.board().get_pos(pos_X+X_offset ,pos_Y+Y_offset) == 0  or self.game.board().get_pos(pos_X+X_offset ,pos_Y+Y_offset) == self.game.turn)
        return False
    
    
    def move(self, direction):
        pos_X, pos_Y = self.position
        
        if(self.check_move(direction)) :
            
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
            
            self.game.board().draw_cell(self.position, self.game.turn)
            game.next_turn()
        else:
            print("Apprend à jouer")
            return 1
#############################################################
  


#############################################################
class Game :
    def __init__(self, player1, player2) :
        self._board = Board()
        self._players = [player1, player2]
        self._histo_pos = [[(0,0)],[(7,7)]]
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
        self._players[0].position = (0,0)
        self._players[1].position = (7,7)
        self.state = "Started"
        
        self.board().set_case(self._players[0].position, self._turn[0])
        self.board().set_case(self._players[1].position, self._turn[1])
        #Draw board & players (Django)
    
    def check_state(self):
        if all(list(itertools.chain(*self.board().cases))):
            self.state = "Over"
            
            
            #Check winner & Count points
            #Add victory to winner user
            #Add played game to both users
        
    
            
    
#############################################################
    


#-----------------------------
#           tests


p1 = Player("p1","pass1")
p2 = Player("p2","pass2")

game = Game(p1, p2)

game.starting()

board_print = ""
for i in range(0,8):
    for j in range(0,8):
        board_print += str(game.board().get_pos(i,j)) + " "
    board_print += "\n"
print(board_print)

while game.state != "Over":
    for p in range(0,2):
        if game.state != "Over":
            pl = game.player(p).name + " >"
            
            action = int(input(pl))
            has_moved = game.player(p).move(action)
            while has_moved != None:
                action = int(input(pl))
                has_moved = game.player(p).move(action)
            
            board_print = ""
            for i in range(0,8):
                for j in range(0,8):
                    board_print += str(game.board().get_pos(i,j)) + " "
                board_print += "\n"
            print(board_print)
        
            
            game.check_state()

    