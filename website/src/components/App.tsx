import { useState, useEffect } from 'react';
import Navbar from './Navbar';
import Dashboard from './Dashboard';
import Modal from './Modal';
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
      <Navbar onOpen={modalOpen} />
      <Dashboard />
      {isShowing && <Modal onClose={modalClose} isShowing={isShowing} />}
    </>
  );
}
