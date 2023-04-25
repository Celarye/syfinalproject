import logo from './includes/plant-icon.png';
import data from './data/data.json';
import './App.css';

console.log(data);

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <div>
          <img src={logo} className="App-logo" alt="logo" />
          <h>Plants Management</h>
        </div>
      </header>
      <body>
        <div>
          <h>Global Values:</h>
          <p>{data.global.temp.at(-1)}</p>
          <h>Plant specific values:</h>
          <p>\Data</p>
        </div>
      </body>
      <footer>
        <div>
          <p>
            Made by Celarye using{' '}
            <a href="https://create-react-app.dev/">Create React App</a>
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
