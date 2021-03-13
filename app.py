"""
Server for Tic Tac Toe game
"""
import os
from flask import Flask, send_from_directory, json, request
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Global Variables
PLAYERS = []
BOARD = ['', '', '', '', '', '', '', '', '']
MOVES = 0
VICTOR = None
GAME_OVER = False
PLAY_AGAIN_CHECK = ['not ready', 'not ready']

APP = Flask(__name__, static_folder='./build/static')

APP.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DB = SQLAlchemy(APP)

import models

CORS = CORS(APP, resources={r"/*": {"origins": "*"}})
SOCKET_IO = SocketIO(APP,
                     cors_allowed_origins="*",
                     json=json,
                     manage_session=False)


@APP.route('/', defaults={"filename": "index.html"})
@APP.route('/<path:filename>')
def index(filename):
    """
    End point to serve web application
    """
    return send_from_directory('./build', filename)


@SOCKET_IO.on('disconnect')
def on_disconnect():
    """
    When a socket disconnects, this function finds the player assocatied with
    the disconnecting socket and removes them from the global PLAYERS list.
    Then the new PLAYERS list is emitted to all other sockets to dispaly a new user component.
    """
    global PLAYERS
    for player in PLAYERS:
        if player[1] == request.sid:
            PLAYERS.remove(player)

    print('socket leaving ' + request.sid)
    SOCKET_IO.emit('removePlayer', PLAYERS, broadcast=True)


@SOCKET_IO.on('updatePlayers')
def on_update_players(username):
    """
    When a player logs in with a username, the database is queried using that username.
    If no player is found in the database, then the new user is added to the database.
    The user logging in is then added to the global PLAYERS list. The new PLAYER list is
    then emitted to all other sockets to create a new user component.
    """
    global PLAYERS
    player = models.Player.query.filter_by(username=username).first()
    if player is None:
        new_player = models.Player(username=username)
        DB.session.add(new_player)
        DB.session.commit()

    PLAYERS.append([username, request.sid])
    SOCKET_IO.emit('updatePlayers', PLAYERS, broadcast=True)


@SOCKET_IO.on('move')
def on_move(data):
    """
    When a player X or player O makes a move, the global MOVES count is updated.
    Next the global BOARD array is copied, the side to the right of the new move is
    spliced off the BOARD array with the new move placed at the end. Then the right side is appended
    again using the copied temp array. This new BOARD is emitted to all other sockets to create
    a new Board component.
    """
    global BOARD, MOVES
    MOVES = MOVES + 1
    temp = BOARD
    BOARD = BOARD[0:data['move']['index']]
    BOARD.append(data['move']['symbol'])
    BOARD.extend(temp[data['move']['index'] + 1:])
    SOCKET_IO.emit('move', data, broadcast=True, include_self=False)


@SOCKET_IO.on('initBoard')
def on_init_board(socket_id):
    """
    This function is used to initialize the board for any newly logged in users
    and is emitted to that new user only.
    """
    global BOARD, MOVES, VICTOR, GAME_OVER, PLAY_AGAIN_CHECK
    SOCKET_IO.emit('initBoard', {
        'board': BOARD,
        'moves': MOVES,
        'victor': VICTOR,
        'gameOver': GAME_OVER,
        'playAgainCheck': PLAY_AGAIN_CHECK
    },
                   room=socket_id)


@SOCKET_IO.on('initLeaderboard')
def on_init_leaderboard(socket_id):
    """
    This function is used to initalize the leaderboard for any newly logged in users
    and is emitted to that new user only.
    """
    all_players = models.Player.query.order_by(models.Player.points.desc())
    top_ten = []
    for player in all_players[:10]:
        new_player = {}
        new_player['username'] = player.username
        new_player['points'] = player.points
        top_ten.append(new_player)
    print('initLeaderboard to ' + socket_id)
    SOCKET_IO.emit('initLeaderboard', top_ten, room=socket_id)


@SOCKET_IO.on('victory')
def on_victory(victor_name):
    """
    If a victory is obtained on a move, this function is called to update the database
    and emit the results to all users.
    """
    global VICTOR, GAME_OVER, PLAYERS
    if victor_name == PLAYERS[0][0]:
        db_victor = DB.session.query(
            models.Player).filter_by(username=PLAYERS[0][0]).first()
        db_loser = DB.session.query(
            models.Player).filter_by(username=PLAYERS[1][0]).first()
    else:
        db_victor = DB.session.query(
            models.Player).filter_by(username=PLAYERS[1][0]).first()
        db_loser = DB.session.query(
            models.Player).filter_by(username=PLAYERS[0][0]).first()

    db_victor.points = db_victor.points + 1
    db_loser.points = db_loser.points - 1
    DB.session.commit()
    VICTOR = victor_name
    GAME_OVER = True
    SOCKET_IO.emit('victory', VICTOR, broadcast=True)


@SOCKET_IO.on('updateLeaderboards')
def update_leaderboards():
    """
    This function is called when a victory occurs and sends out the new leaderboard
    to all users.
    """
    all_players = all_players = models.Player.query.order_by(
        models.Player.points.desc())
    top_ten = []
    print(all_players)
    for player in all_players[:10]:
        new_player = {}
        new_player['username'] = player.username
        new_player['points'] = player.points
        top_ten.append(new_player)
    SOCKET_IO.emit('initLeaderboard', top_ten, broadcast=True)


@SOCKET_IO.on('draw')
def on_draw():
    """
    This function is called when a move is the last move, but no victory
    is obtained. The global GAME_OVER boolean is sent to all users to signify the
    end of the game.
    """
    global GAME_OVER
    GAME_OVER = True
    SOCKET_IO.emit('draw', broadcast=True)


@SOCKET_IO.on('playAgain')
def on_play_again(user_type):
    """
    This function is used to update the play again check for all users to display
    when one or both users are ready to reset and play again.
    """
    global PLAY_AGAIN_CHECK, BOARD, MOVES, GAME_OVER, VICTOR
    prev = PLAY_AGAIN_CHECK
    if user_type == 'X':
        PLAY_AGAIN_CHECK = ['ready', prev[1]]
    elif user_type == 'O':
        PLAY_AGAIN_CHECK = [prev[0], 'ready']

    if PLAY_AGAIN_CHECK[0] == 'ready' and PLAY_AGAIN_CHECK[1] == 'ready':
        BOARD = ['', '', '', '', '', '', '', '', '']
        MOVES = 0
        VICTOR = None
        GAME_OVER = False
        PLAY_AGAIN_CHECK = ['not ready', 'not ready']

    SOCKET_IO.emit('playAgain', user_type, broadcast=True)


# Note we need to add this line so we can import app in the python shell
if __name__ == "__main__":
    SOCKET_IO.run(
        APP,
        host=os.getenv('IP', '0.0.0.0'),
        port=8081 if os.getenv('C9_PORT') else int(os.getenv('PORT', 8081)),
    )
