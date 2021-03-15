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
    When a socket disconnects, call remove_player
    """
    global PLAYERS
    PLAYERS = remove_player(PLAYERS, request.sid)


    SOCKET_IO.emit('removePlayer', PLAYERS, broadcast=True)

def remove_player(players, sid):
    """
    this function finds the player assocatied with
    the disconnecting socket and removes them from the global PLAYERS list.
    Then the new PLAYERS list is emitted to all other sockets to dispaly a new user component.
    """
    for player in players:
        if player[1] == sid:
            players.remove(player)
            break
    return players

@SOCKET_IO.on('updatePlayers')
def on_update_players(username):
    """
    When a player logs in with a username, check if its a new user.
    The user logging in is then added to the global PLAYERS list. The new PLAYER list is
    then emitted to all other sockets to create a new user component.
    """
    global PLAYERS
    player = models.Player.query.filter_by(username=username).first()
    if player is None:
        add_player(username)
    PLAYERS.append([username, request.sid])
    SOCKET_IO.emit('updatePlayers', PLAYERS, broadcast=True)

def add_player(username):
    """
    the database is queried using the username and if no player
    is found in the database, then the new user is added to the database.
    """
    new_player = models.Player(username=username)
    DB.session.add(new_player)
    DB.session.commit()

@SOCKET_IO.on('move')
def on_move(data):
    """
    When a player X or player O makes a move, the global MOVES count is updated.
    Next the global BOARD array is updated by the update_board function
    """
    global BOARD, MOVES
    MOVES = MOVES + 1
    BOARD = update_board(BOARD, data['move']['index'], data['move']['symbol'])
    SOCKET_IO.emit('move', data, broadcast=True, include_self=False)

def update_board(board, move_index, symbol):
    """
    The side to the right of the new move is
    spliced off the BOARD array with the new move placed at the end. Then the right side is appended
    again using the copied temp array. This new BOARD is emitted to all other sockets to create
    a new Board component.
    """
    new_board = board[0:move_index]
    new_board.append(symbol)
    new_board.extend(board[move_index + 1:])
    return new_board

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
    top_ten = get_top_players(10)
    SOCKET_IO.emit('initLeaderboard', top_ten, room=socket_id)

@SOCKET_IO.on('updateLeaderboards')
def update_leaderboards():
    """
    This function is called when a victory occurs and sends out the new leaderboard
    to all users.
    """
    top_ten = get_top_players(10)
    SOCKET_IO.emit('initLeaderboard', top_ten, broadcast=True)

def get_top_players(amount):
    """
    Function to get player from database
    """
    all_players = models.Player.query.order_by(models.Player.points.desc())
    top_ten = []
    for player in all_players[:amount]:
        new_player = {}
        new_player['username'] = player.username
        new_player['points'] = player.points
        top_ten.append(new_player)
    return top_ten

@SOCKET_IO.on('victory')
def on_victory(victor_name):
    """
    If a victory is obtained on a move, this function is called to update the database
    and emit the results to all users.
    """
    global VICTOR, GAME_OVER
    if victor_name == PLAYERS[0][0]:
        update_points(PLAYERS[0][0], PLAYERS[1][0])
    else:
        update_points(PLAYERS[1][0], PLAYERS[0][0])
    VICTOR = victor_name
    GAME_OVER = True
    SOCKET_IO.emit('victory', VICTOR, broadcast=True)

def update_points(victor_name, loser_name):
    """
    Updates winner and losers points in the databse
    """
    db_victor = DB.session.query(
        models.Player).filter_by(username=victor_name).first()
    db_loser = DB.session.query(
        models.Player).filter_by(username=loser_name).first()
    print(db_victor)
    db_victor.points = db_victor.points + 1
    db_loser.points = db_loser.points - 1
    DB.session.commit()


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
    check who is ready by calling the function and then reset game when both players are ready
    """
    global PLAY_AGAIN_CHECK, BOARD, MOVES, GAME_OVER, VICTOR
    PLAY_AGAIN_CHECK = check_whos_ready(PLAY_AGAIN_CHECK, user_type)
    if PLAY_AGAIN_CHECK[0] == 'ready' and PLAY_AGAIN_CHECK[1] == 'ready':
        BOARD = ['', '', '', '', '', '', '', '', '']
        MOVES = 0
        VICTOR = None
        GAME_OVER = False
        PLAY_AGAIN_CHECK = ['not ready', 'not ready']

    SOCKET_IO.emit('playAgain', user_type, broadcast=True)

def check_whos_ready(play_again_check, user_type):
    """
    This function checks to see what player type is ready'ing
    up and updating the play_again_check array
    """
    prev = play_again_check
    if user_type == 'X':
        play_again_check = ['ready', prev[1]]
    elif user_type == 'O':
        play_again_check = [prev[0], 'ready']
    return play_again_check


# Note we need to add this line so we can import app in the python shell
if __name__ == "__main__":
    SOCKET_IO.run(
        APP,
        host=os.getenv('IP', '0.0.0.0'),
        port=8081 if os.getenv('C9_PORT') else int(os.getenv('PORT', 8081)),
    )
