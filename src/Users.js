import React from 'react';
import PropTypes from 'prop-types';
import './Users.css';

function Users(props) {
  const {
    players,
  } = props;
  if (players.length === 1) {
    return (
      <div className="user-container">
        <h2>Player List</h2>
        <p>{`Player X: ${players[0][0]}`}</p>
      </div>
    );
  }
  if (players.length === 2) {
    return (
      <div className="user-container">
        <h2>Player List</h2>
        <p>{`Player X: ${players[0][0]}`}</p>
        <p>{`Player O: ${players[1][0]}`}</p>
      </div>
    );
  }
  if (players.length >= 2) {
    return (
      <div className="user-container">
        <h2>Player List</h2>
        <p>{`Player X: ${players[0][0]}`}</p>
        <p>{`Player O: ${players[1][0]}`}</p>
        <h5>Queue</h5>
        {players.slice(2).map((player, index) => <p key={index}>{`${index + 1} ${player[0]}`}</p>)}
      </div>
    );
  }
  return null;
}

Users.propTypes = {
  players: PropTypes.arrayOf(PropTypes.arrayOf(PropTypes.string)).isRequired,
};

export default Users;
