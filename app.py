import os
from flask import Flask, send_from_directory, json, session, request
from flask_socketio import SocketIO
from flask_cors import CORS

players = []

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
    print('connection players', players)
    print(request.sid)
    socketio.emit('updatePlayers', players, broadcast=True)


@socketio.on('disconnect')
def on_disconnect():
    global players
    for player in players:
        if player[1] == request.sid:
            players.remove(player)
            print(players)
            
    socketio.emit('removePlayer', players, broadcast=True)
    print('disconnected players', players)
    print(request.sid)

@socketio.on('updatePlayers')
def on_update_players(username):
    global players
    players.append([username, request.sid])
    socketio.emit('updatePlayers',  players, broadcast=True, include_self=False)
    print('updated players', players)


@socketio.on('move')
def on_move(data):
    print(str(data))
    socketio.emit('move',  data, broadcast=True, include_self=False)


socketio.run(
    app,
    host=os.getenv('IP', '0.0.0.0'),
    port=8081 if os.getenv('C9_PORT') else int(os.getenv('PORT', 8081)),
)