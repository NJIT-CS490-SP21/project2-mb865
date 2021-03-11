import "./App.css";
import { useState, useEffect } from "react";
import io from "socket.io-client";
import { Board } from "./Board.js";
import { Login } from "./Login.js";
import { Header } from "./Header.js";

const socket = io(); // Connects to socket connection

function App() {
  const [username, setUsername] = useState(null);
  const [userType, setUserType] = useState(null);
  const [players, setPlayers] = useState([]);

  function onLogin(inputValue) {
    if (inputValue != null) {
      console.log("logging in");
      const username =
        inputValue[0].toUpperCase() + inputValue.slice(1).toLowerCase();
      setUsername(username);
      // setPlayers(prevPlayers => [...prevPlayers, [username, socket.id]]);
      socket.emit("initBoard", socket.id);
    }
  }

  function findUserType(position) {
    if (position == 0) {
      setUserType("X");
    } else if (position == 1) {
      setUserType("O");
    } else {
      setUserType("spectator");
    }
    console.log("found player type");
  }

  useEffect(() => {
    if (username !== null) {
      console.log("updating players");
      socket.emit("updatePlayers", username);
    }
  }, [username]);

  useEffect(() => {
    if (username !== null && userType === null && players.length > 0) {
      console.log("finding type");
      findUserType(players.length - 1);
    }
  }, [players]);

  useEffect(() => {
    socket.on("updatePlayers", (updatedPlayers) => {
      setPlayers(updatedPlayers);
      socket.emit("initLeaderboard", socket.id);
    });
    socket.on("removePlayer", (updatedPlayers) => {
      setPlayers(updatedPlayers);
      const findPlayer = (player) => player[1] == socket.id;
      const position = updatedPlayers.findIndex(findPlayer);
      findUserType(position);
      console.log("removing player, getting new type");
    });
  }, []);

  if (username !== null)
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
  else
    return (
      <div>
        <Header />
        <Login onLogin={onLogin} />
      </div>
    );
}

export default App;
