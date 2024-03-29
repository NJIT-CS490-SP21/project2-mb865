import { React, useState, useEffect } from 'react';
import io from 'socket.io-client';
import Board from './Board';
import Login from './Login';
import Header from './Header';
import './App.css';

const socket = io(); // Connects to socket connection

function App() {
  const [username, setUsername] = useState('');
  const [userType, setUserType] = useState('');
  const [players, setPlayers] = useState([]);

  function onLogin(inputValue) {
    if (inputValue !== null) {
      const aUsername = inputValue[0].toUpperCase() + inputValue.slice(1).toLowerCase();
      setUsername(aUsername);
      socket.emit('initBoard', socket.id);
    }
  }

  function findUserType(position) {
    if (position === 0) {
      setUserType('X');
    } else if (position === 1) {
      setUserType('O');
    } else {
      setUserType('spectator');
    }
  }

  useEffect(() => {
    if (username !== '') {
      socket.emit('updatePlayers', username);
    }
  }, [username]);

  useEffect(() => {
    if (username !== '' && userType === '' && players.length > 0) {
      findUserType(players.length - 1);
    }
  }, [players]);

  useEffect(() => {
    socket.on('updatePlayers', (updatedPlayers) => {
      setPlayers(updatedPlayers);
      socket.emit('initLeaderboard', socket.id);
    });
    socket.on('removePlayer', (updatedPlayers) => {
      setPlayers(updatedPlayers);
      const findPlayer = (player) => player[1] === socket.id;
      const position = updatedPlayers.findIndex(findPlayer);
      findUserType(position);
    });
  }, []);

  if (username !== '') {
    return (
      <div>
        <Header />
        <Board
          players={players}
          socket={socket}
          userType={userType}
          username={username}
        />
      </div>
    );
  }
  return (
    <div>
      <Header />
      <Login onLogin={onLogin} />
    </div>
  );
}

export default App;
