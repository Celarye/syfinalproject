import { useState, useEffect } from 'react';
import Modal from './Modal';
import '../styles/App.css';
import '../styles/Dashboard.css';

export default function Dashboard() {
  const [isShowing, setIsShowing] = useState(
    localStorage.getItem('isShowing') === 'true' || false
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
      <div className={`overlay${isShowing ? 'Show' : ''}`}></div>
      <button className="Dashboard-button" onClick={modalOpen}>
        Modal
      </button>
      {isShowing && <Modal onClose={modalClose} />}
    </>
  );
}
