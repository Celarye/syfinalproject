import logo from '../includes/logo.png';
import '../styles/App.css';
import '../styles/Main.css';

export default function Main() {
  return (
    <>
      <img src={logo} className="Main-logo App-logo" alt="logo" />
      <div className="Main">
        <h1>House Plants Manager</h1>
        <p>Automate your house plant management!</p>
        <a href="/Dashboard">
          <button className="Main-button" type="button">
            Dashboard
          </button>
        </a>
      </div>
    </>
  );
}
