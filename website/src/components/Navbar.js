import { useRef } from 'react';
import { FaBars, FaTimes } from 'react-icons/fa';
import logo from '../includes/logo.png';
import '../styles/main.css';
import '../styles/navbar.css';

function Navbar() {
  const navRef = useRef();

  const showNavBar = () => {
    navRef.current.classList.toggle('responsive_nav');
  };

  return (
    <header className="Navbar">
      <img src={logo} className="Navbar-logo App-logo" alt="logo" />
      <h3>House Plants Manager</h3>
      <nav ref={navRef}>
        <a href="/Dashboard">Dashboard</a>
        <a href="/Plant1">Plant 1</a>
        <a href="/Plant2">Plant 2</a>
        <a href="/Plant3">Plant 3</a>
        <button className="nav-btn nav-close-btn" onClick={showNavBar}>
          <FaTimes />
        </button>
      </nav>
      <button className="nav-btn" onClick={showNavBar}>
        <FaBars />
      </button>
    </header>
  );
}

export default Navbar;
