import { useState } from 'react';
import './Leaderboard.css';

export function Leaderboard(props) {
    const [showTopTen, setShowTopTen] = useState(false);
    
    function onToggleTopTen() {
        console.log(props.topTen);
        setShowTopTen((prevIsShown) => {
          return !prevIsShown;
        });
    }

  
  return (
      <div >
        <h2>Leaderboard</h2>
        <button onClick={onToggleTopTen}>Show top 10</button>
        {showTopTen === true ? (
        <div>
          <table>
            <thead>
                <tr>
                  <th>Username</th>
                  <th>Points</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>username</td>
                    <td>points</td>
                </tr>
                <tr>
                    <td>username</td>
                    <td>points</td>
                </tr>
                <tr>
                    <td>username</td>
                    <td>points</td>
                </tr>
                <tr>
                    <td>username</td>
                    <td>points</td>
                </tr>
            </tbody>
          </table>
        </div>
      ) : (
        <div></div>
      )}
      </div>
  );
}
