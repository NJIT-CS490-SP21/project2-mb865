import './Users.css';

export function Users(props) {
    if (props.players.length == 1) {
        return (
            <div className="user-container">
                <h2>Player List</h2>
                <p>Player X: {props.players[0][0]}</p>
            </div>
        );
    } else if (props.players.length == 2) {
        return (
            <div className="user-container">
                <h2>Player List</h2>
                <p>Player X: {props.players[0][0]}</p>
                <p>Player O: {props.players[1][0]}</p>
            </div>
        );
    } else {
        return (
            <div className="user-container">
                <h2>Player List</h2>
                <p>Player X: {props.players[0][0]}</p>
                <p>Player O: {props.players[1][0]}</p>
                <h5>Queue</h5>
                {props.players.map((player, index) => {
                   if (index > 1) {
                       return <p key={index}>{--index + ' ' + player[0]}</p>
                   }
                })}
            </div>
        );
    }
  
}
