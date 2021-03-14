import React from 'react';
import {
  render,
  waitFor,
  screen,
  fireEvent,
} from '@testing-library/react';
import App from './App';
import Box from './Box';
import onClickBox from './Board';

test('Enter button disappears', () => {
  const { container } = render(<App />);
  const EnterButton = screen.getByText('Enter');
  const inputNode = container.querySelector('input');
  inputNode.value = 'Mike';
  expect(EnterButton).toBeInTheDocument();
  fireEvent.click(EnterButton);
  expect(EnterButton).not.toBeInTheDocument();
});

test('Check if username and type are there', async () => {
  const { container } = render(<App />);
  const EnterButton = screen.getByText('Enter');
  const inputNode = container.querySelector('input');
  inputNode.value = 'Joe';
  fireEvent.click(EnterButton);
  await waitFor(() => screen.getByText('Joe ()'));
  expect(screen.getByText('Joe ()')).toBeInTheDocument();
});

test('Check if partially filled board is rendered properly', async () => {
  const board = ['X', '', '', 'O', '', '', '', '', ''];
  render(
    <div className="board-container">
      <div className="board">
        {board.map((piece, index) => (
          <Box
            onClick={onClickBox}
            key={index}
            piece={piece}
            tabIndex={index}
          />
        ))}
      </div>
    </div>,
  );
  const Xbox = screen.getByText('X');
  const Obox = screen.getByText('O');
  expect(Xbox).toBeInTheDocument();
  expect(Obox).toBeInTheDocument();
});
