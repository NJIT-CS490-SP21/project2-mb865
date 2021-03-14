import PropTypes from 'prop-types';
import { React } from 'react';
import './Box.css';

function Box(props) {
  const {
    onClick,
    piece,
    tabIndex,
  } = props;
  return (
      <div tabIndex={tabIndex} role="button" className="box" onClick={onClick} onKeyDown={onClick}>
        {piece === 'X' ? (
          <span className="piece x">{piece}</span>
        ) : (
          <span className="piece o">{piece}</span>
        )}
      </div>
    );
}

Box.propTypes = {
  onClick: PropTypes.func.isRequired,
  piece: PropTypes.string.isRequired,
  tabIndex: PropTypes.number.isRequired,
};

export default Box;
