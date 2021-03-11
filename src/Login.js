import { React, useRef } from 'react';
import PropTypes from 'prop-types';
import './Login.css';

function Login(props) {
  const {
    onLogin,
  } = props;
  const inputRef = useRef(null); // Reference to <input> element

  return (
    <div className="login-container">
      <input type="text" placeholder="Username" ref={inputRef} />
      <br />
      <button
        type="submit"
        onClick={() => onLogin(inputRef.current.value)}
      >
        Enter
      </button>
    </div>
  );
}

Login.propTypes = {
  onLogin: PropTypes.func.isRequired,
};

export default Login;
