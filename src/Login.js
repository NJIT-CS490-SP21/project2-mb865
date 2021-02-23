import React from 'react';
import './Login.css';

export function Login() {

    function onSubmit() {
        
    }
  
    return (
        <div className="login-container">
            <input type="text" placeholder="Username"/><br/>
            <button type="submit" onClick={onSubmit}>Enter</button>
        </div>
    );
}
