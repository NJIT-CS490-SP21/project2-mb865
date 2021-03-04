import { useState } from 'react';
import './Leaderboard.css';

export function Leaderboard(props) {
    const [showTopTen, setShowTopTen] = useState(false);
    
    function onToggleTopTen() {
      console.log(props.username);
        setShowTopTen((prevIsShown) => {
          return !prevIsShown;
        });
    }

  
  return (
      <div >
        <h2>Leaderboard</h2>
        {showTopTen === true ? (
        <div>
        <button onClick={onToggleTopTen}>Hide top 10</button>
          <table>
            <thead>
                <tr>
                  <th>Username</th>
                  <th>Points</th>
                </tr>
            </thead>
            <tbody>
               {props.topTen.map((player, index) => {
                return  <tr key={index}>
                          <td className={props.username == player.username ? 'you' : ''}>{++index}. {player.username}</td>
                          <td className={props.username == player.username ? 'you' : ''}>{player.points}</td>
                        </tr>
                })}
            </tbody>
          </table>
        </div>
      ) : (
        <div><button onClick={onToggleTopTen}>Show top 10</button></div>
      )}
      </div>
  );
}
