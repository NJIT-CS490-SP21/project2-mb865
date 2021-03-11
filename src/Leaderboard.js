import { React, useState } from 'react';
import PropTypes from 'prop-types';
import './Leaderboard.css';

function Leaderboard(props) {
  const [showTopTen, setShowTopTen] = useState(false);
  const {
    topTen,
    username,
  } = props;

  function onToggleTopTen() {
    setShowTopTen((prevIsShown) => !prevIsShown);
  }

  return (
    <div>
      <h2>Leaderboard</h2>
      {showTopTen === true ? (
        <div>
          <button type="button" onClick={onToggleTopTen}>Hide top 10</button>
          <table>
            <thead>
              <tr>
                <th>Username</th>
                <th>Points</th>
              </tr>
            </thead>
            <tbody>
              {topTen.map((player, index) => (
                <tr key={index}>
                  <td
                    className={username === player.username ? 'you' : ''}
                  >
                    {`${index + 1}. ${player.username}`}
                  </td>
                  <td
                    className={username === player.username ? 'you' : ''}
                  >
                    {player.points}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div>
          <button type="button" onClick={onToggleTopTen}>Show top 10</button>
        </div>
      )}
    </div>
  );
}

Leaderboard.propTypes = {
  topTen: PropTypes.arrayOf(PropTypes.shape({
    username: PropTypes.string,
    points: PropTypes.number,
  })).isRequired,
  username: PropTypes.string.isRequired,
};

export default Leaderboard;
