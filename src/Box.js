import React from 'react';
import { useState } from 'react';
import './Box.css';

export function Box(props) {

  
  return (
      <div className="box" onClick={props.onClick}>
        {props.piece === 'X' ? <span className="piece x">{props.piece}</span> : <span className="piece o">{props.piece}</span>}
      </div>
  );
}
