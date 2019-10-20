

class Board :
    def __init__(self) :
        self._cases = [[0 for col in range(0,8)] for row in range(0,8)]
    





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
    





class Player (User):
    def __init__(self, name, password) :
        super.__init__(name, password)
        self._position = []
        self._is_human
    
    
    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self,pos):
        self._position = pos
    
    
    def move(self, direction):
        if direction == 1:
            #go left
        elif direction == 2:
            #go right
        elif direction == 3:
            #go up
        else:
            #go down
            
        



class Game :
    def __init__(self, player1, player2) :
        self._board = Board()
        self._players = [player1, player2]
        self._histo_pos = [[(0,0)]],[[(7,7)]]
        self._turn = [0,1]
    
    
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
    def histo_pos(self):
        return self._histo_pos
    
    @histo_pos.setter
    def histo_pos(self, pos):
        self._histo_pos[self.turn].append(pos)
        
    
    
    def next_turn(self):
        self._turn.reverse()
        
    def starting(self):
        self._players[0].position = (0,0)
        self._players[1].position = (7,7)
        #Draw board & players
        









#-----------------------------
#           tests


p1 = Player("p1","pass1")
p2 = Player("p2","pass2")

game = Game(p1, p2)






