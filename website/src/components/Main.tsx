import logo from '../includes/logo.png';
import '../styles/App.css';
import '../styles/Main.css';

export default function Main() {
  return (
    <>
      <div className="Main">
        <img src={logo} className="Main-logo App-logo" alt="logo" />
        <h1 className="Main-title">House Plants Manager</h1>
        <p className="Main-description">
          Modernize your house plant management!
        </p>
        <div className="Main-info">
          <div className="Main-info-column">
            <h3>Monitoring</h3>
            <p>
              Effortlessly monitor the health of your plants with a
              user-friendly system
            </p>
          </div>
          <div className="Main-info-column Main-info-column2">
            <h3>Automation</h3>
            <p>
              Enable automatic responses on the website based on the conditions
              of your plant
            </p>
          </div>
          <div className="Main-info-column">
            <h3>Notifications</h3>
            <p>
              Stay informed about the condition and care of your plants with
              timely notifications
            </p>
          </div>
        </div>
        <button className="Main-button" type="button">
          Understood!
        </button>
        <footer className="Main-footer">
          <p>
            Made by Celarye using{' '}
            <a className="App-link" href="https://create-react-app.dev/">
              Create React App
            </a>
          </p>
        </footer>
      </div>
    </>
  );
}
