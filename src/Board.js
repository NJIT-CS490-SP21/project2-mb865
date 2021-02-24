import React from 'react';
import { useState, useEffect } from 'react';
import { Box } from './Box.js';
import io from 'socket.io-client';
import './Board.css';

const socket = io(); // Connects to socket connection

export function Board(props) {
  const [board, setBoard] = useState(['','','','','','','','','']);
  const [moves, setMoves] = useState(0);
  
  function onClickBox(index) {
    if (board[index] != '') return;
    
    let symbol = '';
    if (moves <= 9 && moves % 2 == 0) symbol = 'X';
    else if (moves <= 9 && moves % 2 != 0) symbol = 'O';
    
    if (symbol != props.userType) return;
    
    setBoard((prevBoard) => [...prevBoard.slice(0, index), symbol, ...prevBoard.slice(index + 1)]);
    setMoves((prevMoves) => prevMoves + 1);
      
    socket.emit('move', { 
      move: {
        index,
        symbol
      }
    });
    
  }
  
  
  useEffect(() => {
    socket.on('move', (data) => {
      console.log('Move event received!');
      console.log(data);
      setBoard((prevBoard) => [...prevBoard.slice(0, data.move.index), data.move.symbol, ...prevBoard.slice(data.move.index + 1)]);
      setMoves((prevMoves) => prevMoves + 1);
    });
  }, []);

  
  return (
    <div className="board-container">
      <h2>{props.userType}</h2>
      <div className="board">
        {board.map((piece, index) => {
            return <Box onClick={() => onClickBox(index)} key={index} piece={piece} />
        })}
      </div>
    </div>
  );
}