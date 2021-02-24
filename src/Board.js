import React from 'react';
import { useState, useEffect } from 'react';
import { Box } from './Box.js';
import './Board.css';

let lastIndex = 0;

export function Board(props) {
  const [board, setBoard] = useState(['','','','','','','','','']);
  const [moves, setMoves] = useState(0);
  const [victory, setVictory] = useState(false);
  const [victor, setVictor] = useState(null);
  
  function onClickBox(index) {
    if (board[index] != '' || victory) return;
    
    let symbol = '';
    if (moves <= 9 && moves % 2 == 0) symbol = 'X';
    else if (moves <= 9 && moves % 2 != 0) symbol = 'O';
    
    if (symbol != props.userType) return;
    
    setBoard((prevBoard) => [...prevBoard.slice(0, index), symbol, ...prevBoard.slice(index + 1)]);
    setMoves((prevMoves) => prevMoves + 1);
    lastIndex = index;
    props.socket.emit('move', { 
      move: {
        index,
        symbol
      }
    });
  }
  
  function checkIfWon(index) {
    if (moves < 5) return false;
    
    const verticalCheck = board[index] + board[(index + 3) % 9] + board[(index + 6) % 9]
    
    const horizontalRanges = [[0,1,2],[3,4,5],[6,7,8]];
    let horizontalCheck = '';
    for (let i = 0; i < 3; i++) {
      if (horizontalRanges[i].includes(index)) {
        horizontalCheck = board[horizontalRanges[i][0]] + board[horizontalRanges[i][1]] + board[horizontalRanges[i][2]]
        break;
      }
    }
    
    const checkMainDiagonal = [0,4,8].includes(index);
    const mainDiagonalCheck = board[0] + board[4] + board[8]
    
    const checkSideDiagonal = [2,4,6].includes(index);
    const sideDiagonalCheck = board[2] + board[4] + board[6]
    
    // check if previous move caused a win on vertical line 
    if (verticalCheck === 'XXX' || verticalCheck === 'OOO') {
      return true;
    }


    // check if previous move caused a win on horizontal line 
    if (horizontalCheck === 'XXX' || horizontalCheck === 'OOO') {
      return true;
    }

    // check if previous move was on the main diagonal and caused a win
    if (checkMainDiagonal && (mainDiagonalCheck === 'XXX' || mainDiagonalCheck === 'OOO')) {
      return true
    }

    // check if previous move was on the secondary diagonal and caused a win
    if (checkSideDiagonal && (sideDiagonalCheck === 'XXX' || sideDiagonalCheck === 'OOO')) {
      return true
    }
  }
  
  useEffect(() => {
    if (checkIfWon(lastIndex)) {
      props.socket.emit('victory', props.username)
    }
  }, [board]);
  
  
  useEffect(() => {
    props.socket.on('move', (data) => {
      console.log('Move event received!');
      console.log(data);
      setBoard((prevBoard) => [...prevBoard.slice(0, data.move.index), data.move.symbol, ...prevBoard.slice(data.move.index + 1)]);
      setMoves((prevMoves) => prevMoves + 1);
    });
    props.socket.on('victory', (victor) => {
      console.log("VICTORY!!!!");
      setVictor(victor);
      setVictory(true);
    });
  }, []);

  if (!victory) 
    return (
      <div className="board-container">
        <h2>{props.username} ({props.userType})</h2>
        <div className="board">
          {board.map((piece, index) => {
              return <Box onClick={() => onClickBox(index)} key={index} piece={piece} />
          })}
        </div>
      </div>
    );
  else
    return (
      <div className="board-container">
        <h2>{props.username} ({props.userType})</h2>
        <h3>{victory ? victor + ' has won!' : ''}</h3>
        <button>Play Again?</button>
        <div className="board">
          {board.map((piece, index) => {
              return <Box onClick={() => onClickBox(index)} key={index} piece={piece} />
          })}
        </div>
      </div>
    );
}