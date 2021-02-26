import os
from flask import Flask, send_from_directory, json, session, request
from flask_socketio import SocketIO
from flask_cors import CORS

players = []
board = ['', '', '', '', '', '', '', '', '']
moves = 0
victor = None
gameOver = False
playAgainCheck = ['not ready', 'not ready']

app = Flask(__name__, static_folder='./build/static')

cors = CORS(app, resources={r"/*": {"origins": "*"}})

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    json=json,
    manage_session=False
)


@app.route('/', defaults={"filename": "index.html"})
@app.route('/<path:filename>')
def index(filename):
    return send_from_directory('./build', filename)


@socketio.on('connect')
def on_connect():
    global players
    socketio.emit('updatePlayers', players, broadcast=True)


@socketio.on('disconnect')
def on_disconnect():
    global players
    for player in players:
        if player[1] == request.sid:
            players.remove(player)
    socketio.emit('removePlayer', players, broadcast=True)


@socketio.on('updatePlayers')
def on_update_players(username):
    global players
    players.append([username, request.sid])
    socketio.emit('updatePlayers',  players, broadcast=True, include_self=False)


@socketio.on('move')
def on_move(data):
    global board, moves
    moves = moves + 1
    temp = board
    board = board[0:data['move']['index']]
    board.append(data['move']['symbol'])
    board.extend(temp[data['move']['index'] + 1:])
    socketio.emit('move',  data, broadcast=True, include_self=False)
    
@socketio.on('initBoard')
def on_init_board(socketId):
    global board, moves, victor, gameOver
    socketio.emit('initBoard', {'board': board, 'moves': moves, 'victor': victor, 'gameOver': gameOver, 'playAgainCheck': playAgainCheck}, room=socketId)
    
@socketio.on('victory')
def on_victory(victorName):
    global victor, gameOver
    victor = victorName
    gameOver = True
    socketio.emit('victory', victor, broadcast=True)
    
@socketio.on('draw')
def on_draw():
    global victor, gameOver
    gameOver = True
    socketio.emit('draw', broadcast=True)

@socketio.on('playAgain')
def on_play_again(userType):
    global playAgainCheck, board, moves, gameOver, victor
    prev = playAgainCheck
    if userType == 'X':
        playAgainCheck = ['ready', prev[1]]
    elif userType == 'O':
        playAgainCheck = [prev[0], 'ready']
        
    if playAgainCheck[0] == 'ready' and playAgainCheck[1] == 'ready':
        print('reseting board in server')
        board = ['', '', '', '', '', '', '', '', '']
        moves = 0
        victor = None
        gameOver = False
        playAgainCheck = ['not ready', 'not ready']
        
    socketio.emit('playAgain', userType, broadcast=True)
    
socketio.run(
    app,
    host=os.getenv('IP', '0.0.0.0'),
    port=8081 if os.getenv('C9_PORT') else int(os.getenv('PORT', 8081)),
)