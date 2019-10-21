


#############################################################
class Board :
    def __init__(self) :
        self._cases = [[0 for col in range(0,8)] for row in range(0,8)]
        
        
    @property
    def cases(self) :
        return self._cases    
    
    
    def draw_cell(self, pos, player_value) :
        x,y = pos
        self.cases[x][y] = player_value
#############################################################
       
   
     
#############################################################     
class User :
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
        super.__init__(name, password)
        self._position = []
        self._is_human
        self._game
    
    
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
        if direction == 1:
            X_offset = 0
            Y_offset = -1
        elif direction == 2:
            X_offset = 0
            Y_offset = 1
        elif direction == 3:
            X_offset = -1
            Y_offset = 0
        else :
            X_offset = 1
            Y_offset = 0
            
        if((pos_X+X_offset >= 0 and pos_X+X_offset <= 7) and (pos_Y+Y_offset >=0 and pos_Y+Y_offset <= 7)):
            return (self.game.board.get_pos(pos_X+X_offset ,pos_Y+Y_offset) != self.game.turn and (self.game.board.get_pos(pos_X+X_offset ,pos_Y+Y_offset) != 0 ))
        return False
    
    
    def move(self, direction):
        pos_X, pos_Y = self.position
        if(self.check_move(direction)) :
            if direction == 1:
                self.position = (pos_X, pos_Y-1)
                self.game.histo_pos((pos_X, pos_Y-1))
            elif direction == 2:
                self.position = (pos_X, pos_Y+1)
                self.game.histo_pos((pos_X, pos_Y+1))
            elif direction == 3:
                self.position = (pos_X-1, pos_Y)
                self.game.histo_pos((pos_X-1, pos_Y))
            else:
                self.position = (pos_X+1, pos_Y)
                self.game.histo_pos((pos_X+1, pos_Y))
            self.game.board.draw_cell(self.position, self.game.turn)
            self.game.next_turn()
        else:
            print("Apprend à jouer")
#############################################################
  


#############################################################
class Game :
    def __init__(self, player1, player2) :
        self._board = Board()
        self._players = [player1, player2]
        self._histo_pos = [[(0,0)]],[[(7,7)]]
        self._turn = [-1,1]
        self._players[0].assign_game(self)
        self._players[1].assign_game(self)
        self._state = "Not Started"
    
    
    @property
    def turn(self):
        return self._turn[0]
    
    
    @property
    def board(self):
        return self._board
    
    
    @property
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
        self.player.reverse()
        
    def starting(self):
        self._players[0].position = (0,0)
        self._players[1].position = (7,7)
        self.state = "Started"
        #Draw board & players (Django)
    
    def check_state(self):
        if not(0 in self.board.cases):
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






