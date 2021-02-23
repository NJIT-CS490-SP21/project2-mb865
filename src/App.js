import logo from './logo.svg';
import './App.css';
import { useState } from 'react';
import { Board } from './Board.js';
import { Login } from './Login.js';
import { Header } from './Header.js';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  if (isLoggedIn)
    return (
      <div>
        <Header />
        <Board />
      </div>
    );
  else
    return (
      <div>
        <Header />
        <Login />
      </div>
    );
}

export default App;
