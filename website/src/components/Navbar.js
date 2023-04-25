import logo from '../includes/plant-icon.png';
import { useRef } from 'react';
import { FaBars, FaTimes } from 'react-icons/fa';

function Navbar() {
  const navRef = useRef();

  const showNavBar = () => {
    navRef.current.classList.toggle('responsive_nav');
  };

  return (
    <header>
      <img src={logo} className="App-logo" alt="logo" />
      <h3>House Plants Manager</h3>
      <nav ref={navRef}>
        <a href="/#">Dashboard</a>
        <a href="/#">Plant 1</a>
        <a href="/#">Plant 2</a>
        <a href="/#">Plant 3</a>
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
