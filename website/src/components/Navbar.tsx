import { useRef } from 'react';
import { ModalProps } from './App';
import logo from '../includes/logo.png';
import { FaBars, FaTimes } from 'react-icons/fa';
import '../styles/Navbar.css';

export default function Navbar(props: ModalProps) {
  function modalOpen() {
    props?.onOpen?.();
  }

  const navRef = useRef<HTMLDivElement>(null);

  const showNavBar = () => {
    navRef.current?.classList.toggle('responsive_nav');
  };

  return (
    <>
      <header className="Navbar">
        <img src={logo} className="Navbar-logo App-logo" alt="logo" />
        <h3>House Plants Manager</h3>
        <nav ref={navRef}>
          <button className="Modal-button" onClick={modalOpen}>
            Info
          </button>
          <button
            title="NavbarClose"
            className="nav-btn nav-close-btn"
            onClick={showNavBar}
          >
            <FaTimes />
          </button>
        </nav>
        <button title="NavbarExpand" className="nav-btn" onClick={showNavBar}>
          <FaBars />
        </button>
      </header>
    </>
  );
}
