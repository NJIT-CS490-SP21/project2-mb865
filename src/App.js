import logo from './logo.svg';
import './App.css';
import { useState, useEffect } from 'react';
import io from 'socket.io-client';
import { Board } from './Board.js';
import { Login } from './Login.js';
import { Header } from './Header.js';

const socket = io(); // Connects to socket connection

function App() {
  const [username, setUsername] = useState(null);
  const [userType, setUserType] = useState(null);
  const [players, setPlayers] = useState([]);
  
  function onLogin(inputValue) {
    if (inputValue != null) {
      console.log('setting username');
      setUsername(inputValue);
      setPlayers(prevPlayers => [...prevPlayers, inputValue]);
    }
  }
  
  function findUserType() {
    console.log(players)
    if (players.length == 1) {
      console.log('I am player X');
      setUserType('X');
    } else if (players.length == 2) {
      console.log('I am player O');
      setUserType('O');
    } else {
      console.log('I am a spectator');
      setUserType('spectator');
    }
  }
  
  useEffect(() => { 
    if (username) {
      console.log(username + ' is set');
      console.log('Tell everyone im logged in');
      findUserType()
      socket.emit('login', username);
    }
  }, [username])
  
  useEffect(() => {
    socket.on('login', (players) => {
      console.log('Time to update my players');
      setPlayers(players)
    });
  }, []);

  if (username)
    return (
      <div>
        <Header />
        <Board userType = {userType}/>
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
