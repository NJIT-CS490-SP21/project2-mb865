import os
from flask import Flask, send_from_directory, json, request
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Global Variables
players = []
board = ['', '', '', '', '', '', '', '', '']
moves = 0
victor = None
gameOver = False
playAgainCheck = ['not ready', 'not ready']

app = Flask(__name__, static_folder='./build/static')

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

import models

cors = CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app,
                    cors_allowed_origins="*",
                    json=json,
                    manage_session=False)


@app.route('/', defaults={"filename": "index.html"})
@app.route('/<path:filename>')
def index(filename):
    return send_from_directory('./build', filename)


@socketio.on('connect')
def on_connect():
    # global players
    # socketio.emit('updatePlayers', players, broadcast=True)
    print('new socket ' + request.sid)


@socketio.on('disconnect')
def on_disconnect():
    global players
    for player in players:
        if player[1] == request.sid:
            players.remove(player)

    print('socket leaving ' + request.sid)
    socketio.emit('removePlayer', players, broadcast=True)


@socketio.on('updatePlayers')
def on_update_players(username):
    global players
    player = models.Player.query.filter_by(username=username).first()
    if player == None:
        newPlayer = models.Player(username=username)
        db.session.add(newPlayer)
        db.session.commit()
        print("new player added into db")

    players.append([username, request.sid])
    print('updatePlayers to all sockets')
    socketio.emit('updatePlayers', players, broadcast=True)


@socketio.on('move')
def on_move(data):
    global board, moves
    moves = moves + 1
    temp = board
    board = board[0:data['move']['index']]
    board.append(data['move']['symbol'])
    board.extend(temp[data['move']['index'] + 1:])
    socketio.emit('move', data, broadcast=True, include_self=False)


@socketio.on('initBoard')
def on_init_board(socketId):
    global board, moves, victor, gameOver
    print('initBoard to ' + request.sid)
    socketio.emit('initBoard', {
        'board': board,
        'moves': moves,
        'victor': victor,
        'gameOver': gameOver,
        'playAgainCheck': playAgainCheck
    },
                  room=socketId)


@socketio.on('initLeaderboard')
def on_init_leaderboard(socketId):
    all_players = models.Player.query.order_by(models.Player.points.desc())
    top_ten = []
    for player in all_players[:10]:
        newPlayer = {}
        newPlayer['username'] = player.username
        newPlayer['points'] = player.points
        top_ten.append(newPlayer)
    print('initLeaderboard to ' + socketId)
    socketio.emit('initLeaderboard', top_ten, room=socketId)


@socketio.on('victory')
def on_victory(victorName):
    global victor, gameOver, players
    if victorName == players[0][0]:
        db_victor = db.session.query(
            models.Player).filter_by(username=players[0][0]).first()
        db_loser = db.session.query(
            models.Player).filter_by(username=players[1][0]).first()
    else:
        db_victor = db.session.query(
            models.Player).filter_by(username=players[1][0]).first()
        db_loser = db.session.query(
            models.Player).filter_by(username=players[0][0]).first()

    db_victor.points = db_victor.points + 1
    db_loser.points = db_loser.points - 1
    db.session.commit()
    victor = victorName
    gameOver = True
    socketio.emit('victory', victor, broadcast=True)


@socketio.on('updateLeaderboards')
def update_leaderboards():
    all_players = all_players = models.Player.query.order_by(
        models.Player.points.desc())
    top_ten = []
    print(all_players)
    for player in all_players[:10]:
        newPlayer = {}
        newPlayer['username'] = player.username
        newPlayer['points'] = player.points
        top_ten.append(newPlayer)
    socketio.emit('initLeaderboard', top_ten, broadcast=True)


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
        board = ['', '', '', '', '', '', '', '', '']
        moves = 0
        victor = None
        gameOver = False
        playAgainCheck = ['not ready', 'not ready']

    socketio.emit('playAgain', userType, broadcast=True)


# Note we need to add this line so we can import app in the python shell
if __name__ == "__main__":
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=8081 if os.getenv('C9_PORT') else int(os.getenv('PORT', 8081)),
    )
