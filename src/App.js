import logo from './logo.svg';
import './App.css';
import { useState, useEffect } from 'react';
import io from 'socket.io-client';
import { Board } from './Board.js';
import { Users } from './Users.js';
import { Login } from './Login.js';
import { Header } from './Header.js';

const socket = io(); // Connects to socket connection

function App() {
  const [username, setUsername] = useState(null);
  const [userType, setUserType] = useState(null);
  const [players, setPlayers] = useState([]);
  
  function onLogin(inputValue) {
    if (inputValue != null) {
      setUsername(inputValue);
      setPlayers(prevPlayers => [...prevPlayers, [inputValue, socket.id]]);
      socket.emit('initBoard', socket.id);
    }
  }
  
  function findUserType(position) {
    if (position == 0) {
      setUserType('X');
    } else if (position == 1) {
      setUserType('O');
    } else {
      setUserType('spectator');
    }
  }
  
  useEffect(() => { 
    if (username) {
      findUserType(players.length - 1);
      socket.emit('updatePlayers', username);
    }
  }, [username])
  
  
  useEffect(() => {
    socket.on('updatePlayers', (updatedPlayers) => {
      setPlayers(updatedPlayers);
    });
    socket.on('removePlayer', (updatedPlayers) => {
      setPlayers(updatedPlayers);
      const findPlayer = (player) => player[1] == socket.id;
      const position = updatedPlayers.findIndex(findPlayer)
      findUserType(position)
    });
  }, []);

  if (username)
    return (
      <div>
        <Header />
        <Board socket = {socket} userType = {userType} username={username}/>
        <Users players = {players}/>
      </div>
    );
  else
    return (
      <div>
        <Header />
        <Login onLogin = {onLogin} />
      </div>
    );
}

export default App;
