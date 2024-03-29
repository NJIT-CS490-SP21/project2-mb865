import { React, useState, useEffect } from 'react';
import io from 'socket.io-client';
import PropTypes from 'prop-types';
import Box from './Box';
import Users from './Users';
import Leaderboard from './Leaderboard';
import './Board.css';

let lastIndex = 0;

function Board(props) {
  const [board, setBoard] = useState(['', '', '', '', '', '', '', '', '']);
  const [moves, setMoves] = useState(0);
  const [gameOver, setGameOver] = useState(false);
  const [victor, setVictor] = useState(null);
  const [playAgainCheck, setPlayAgainCheck] = useState([
    'not ready',
    'not ready',
  ]);
  const [leaderboard, setLeaderboard] = useState([]);
  const {
    username,
    userType,
    players,
    socket,
  } = props;

  function onClickBox(index) {
    if (board[index] !== '' || gameOver) return;

    let symbol = '';
    if (moves <= 9 && moves % 2 === 0) symbol = 'X';
    else if (moves <= 9 && moves % 2 !== 0) symbol = 'O';

    if (symbol !== props.userType) return;

    setBoard((prevBoard) => [
      ...prevBoard.slice(0, index),
      symbol,
      ...prevBoard.slice(index + 1),
    ]);
    setMoves((prevMoves) => prevMoves + 1);
    lastIndex = index;
    socket.emit('move', {
      move: {
        index,
        symbol,
      },
    });
  }

  function gameStatus(index) {
    if (moves < 5) return false;

    const verticalCheck = board[index] + board[(index + 3) % 9] + board[(index + 6) % 9];

    const horizontalRanges = [
      [0, 1, 2],
      [3, 4, 5],
      [6, 7, 8],
    ];
    let horizontalCheck = '';
    for (let i = 0; i < 3; i += 1) {
      if (horizontalRanges[i].includes(index)) {
        horizontalCheck = board[horizontalRanges[i][0]] + board[horizontalRanges[i][1]]
          + board[horizontalRanges[i][2]];
        break;
      }
    }

    const checkMainDiagonal = [0, 4, 8].includes(index);
    const mainDiagonalCheck = board[0] + board[4] + board[8];

    const checkSideDiagonal = [2, 4, 6].includes(index);
    const sideDiagonalCheck = board[2] + board[4] + board[6];

    // check if previous move caused a win on vertical line
    if (verticalCheck === 'XXX' || verticalCheck === 'OOO') {
      return 'victory';
    }

    // check if previous move caused a win on horizontal line
    if (horizontalCheck === 'XXX' || horizontalCheck === 'OOO') {
      return 'victory';
    }

    // check if previous move was on the main diagonal and caused a win
    if (
      checkMainDiagonal
      && (mainDiagonalCheck === 'XXX' || mainDiagonalCheck === 'OOO')
    ) {
      return 'victory';
    }

    // check if previous move was on the secondary diagonal and caused a win
    if (
      checkSideDiagonal
      && (sideDiagonalCheck === 'XXX' || sideDiagonalCheck === 'OOO')
    ) {
      return 'victory';
    }

    // check if a draw
    if (moves === 9) return 'draw';
    return false;
  }

  function onPlayAgain(aUserType) {
    if (aUserType === 'spectator') return;
    socket.emit('playAgain', userType);
  }

  function reset() {
    setBoard(['', '', '', '', '', '', '', '', '']);
    setMoves(0);
    setGameOver(false);
    setVictor(null);
    setPlayAgainCheck(['not ready', 'not ready']);
  }

  useEffect(() => {
    if (gameStatus(lastIndex) === 'victory') {
      socket.emit('victory', props.username);
    } else if (gameStatus(lastIndex) === 'draw') {
      socket.emit('draw');
    }
  }, [board]);

  useEffect(() => {
    if (playAgainCheck[0] === 'ready' && playAgainCheck[1] === 'ready') reset();
  }, [playAgainCheck]);

  useEffect(() => {
    socket.on('initBoard', (boardData) => {
      setBoard(boardData.board);
      setMoves(boardData.moves);
      setGameOver(boardData.gameOver);
      setVictor(boardData.victor);
      setPlayAgainCheck(boardData.playAgainCheck);
    });
    socket.on('initLeaderboard', (topTen) => {
      setLeaderboard(topTen);
    });
    socket.on('move', (data) => {
      setBoard((prevBoard) => [
        ...prevBoard.slice(0, data.move.index),
        data.move.symbol,
        ...prevBoard.slice(data.move.index + 1),
      ]);
      setMoves((prevMoves) => prevMoves + 1);
    });
    socket.on('victory', (aVictor) => {
      if (username === aVictor) socket.emit('updateLeaderboards');
      setVictor(aVictor);
      setGameOver(true);
    });
    socket.on('draw', () => {
      setGameOver(true);
    });
    socket.on('playAgain', (aUserType) => {
      if (aUserType === 'X') {
        setPlayAgainCheck((prev) => ['ready', prev[1]]);
      } else if (aUserType === 'O') {
        setPlayAgainCheck((prev) => [prev[0], 'ready']);
      }
    });
  }, []);

  if (!gameOver) {
    return (
      <div className="main-container">
        <h2>
          {`${username}  (${userType})`}
        </h2>
        <div className="board-container">
          <Users players={players} />
          <div className="board">
            {board.map((piece, index) => (
              <Box
                onClick={() => onClickBox(index)}
                key={index}
                piece={piece}
                tabIndex={index}
              />
            ))}
          </div>
          <Leaderboard username={username} topTen={leaderboard} />
        </div>
      </div>
    );
  }
  return (
    <div className="main-container">
      <h2>
        {`${username}  (${userType})`}
      </h2>
      <div className="board-container">
        <Users players={players} />
        <div className="board">
          {board.map((piece, index) => (
            <Box onClick={() => onClickBox(index)} key={index} piece={piece} tabIndex={index} />))}
        </div>
        <Leaderboard username={username} topTen={leaderboard} />
      </div>
      <h3>{victor ? `${victor} has won!` : 'Draw!!'}</h3>
      <h5>{`Player X is ${playAgainCheck[0]} to play again`}</h5>
      <h5>{`Player O is ${playAgainCheck[1]} to play again`}</h5>
      <button type="button" onClick={() => onPlayAgain(userType)}>Play Again?</button>
    </div>
  );
}

Board.propTypes = {
  username: PropTypes.string.isRequired,
  userType: PropTypes.string.isRequired,
  players: PropTypes.arrayOf(PropTypes.arrayOf(PropTypes.string)).isRequired,
  socket: PropTypes.instanceOf(io).isRequired,
};

export default Board;
