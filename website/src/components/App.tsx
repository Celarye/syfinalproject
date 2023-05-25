import { useState, useEffect } from 'react';
import Data from './Data';
import Modal from './Modal';
import logo from '../includes/logo.png';
import '../styles/App.css';

export type ModalProps = {
  onClose?: () => void;
  onOpen?: () => void;
  isShowing?: boolean;
};

export default function App() {
  const [isShowing, setIsShowing] = useState(
    localStorage.getItem('isShowing') === 'false'
      ? false
      : localStorage.getItem('isShowing') === 'true'
      ? true
      : true
  );

  function modalOpen() {
    setIsShowing(true);
  }

  function modalClose() {
    setIsShowing(false);
  }

  useEffect(() => {
    localStorage.setItem('isShowing', isShowing.toString());
  }, [isShowing]);

  return (
    <>
      <img src={logo} className="App-logo" alt="logo" />
      <h1 className="App-title">House Plants Manager</h1>
      <button className="App-button" onClick={modalOpen}>
        Info
      </button>
      <Data />
      <footer>
        Made by{' '}
        <a className="App-link" href="https://github.com/Celarye">
          Celarye
        </a>{' '}
        using{' '}
        <a className="App-link" href="https://create-react-app.dev/">
          Create React App
        </a>
      </footer>
      {isShowing && <Modal onClose={modalClose} isShowing={isShowing} />}
    </>
  );
}
