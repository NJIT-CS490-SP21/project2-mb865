import { useRef } from 'react';
import './Login.css';

export function Login(props) {
    const inputRef = useRef(null); // Reference to <input> element
  
    return (
        <div className="login-container">
            <input type="text" placeholder="Username" ref={inputRef}/><br/>
            <button type="submit" onClick={() => props.onLogin(inputRef.current.value)}>Enter</button>
        </div>
    );
}
