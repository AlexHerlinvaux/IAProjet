from django.shortcuts import render
from app.static.app import game

game_launched = game.game
size_matrix = [i for i in range(1,game.size_matrix + 1)]

def dj_game_ini(request):
    return render(request, 'app/game.html', {
        'size_matrix' : size_matrix,
        'board':game_launched.board().cases,
        'p1':list(game_launched.player(0).position),
        'p2':list(game_launched.player(1).position),
        'status':game_launched.state,
        }
    )

def dj_game(request, input_ = None):
    if input_ in [1,2,3,4]:
        game_launched.play(input_)

        rend = render(request, 'app/game.html', {
                'size_matrix': size_matrix,
                'board':game_launched.board().cases,
                'p1':list(game_launched.player(0).position),
                'p2':list(game_launched.player(1).position),
                'status':game_launched.state,
                }
        )
        
        if game_launched.state == "Over":
            game_launched.restart()
        
        return rend
    else:
        game_launched.restart()
        return render(request, 'app/game.html', {
            'size_matrix' : size_matrix,
            'board':game_launched.board().cases,
            'p1':list(game_launched.player(0).position),
            'p2':list(game_launched.player(1).position),
            'status':game_launched.state,
            }
        )