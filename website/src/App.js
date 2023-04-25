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
          <h>
            <b>Plants Management</b>
          </h>
        </div>
      </header>
      <body className="App-body">
        <div>
          <br></br>
          <p>
            <i>Last fetched: {data.creationDate}</i>
          </p>
          <h>
            <b>Global Values:</b>
          </h>
          <p>Temperature: {data.global.temp.at(-1)}</p>
          <br></br>
          <h>
            <b>Plant specific soil moisture values:</b>
          </h>
          <table className="App-body-table">
            <tr>
              <th>Plant 1</th>
              <th>Plant 2</th>
              <th>Plant 3</th>
            </tr>
            <tr>
              <td>{data.plants.plant1.soilMoisture.at(-1)}</td>
              <td>{data.plants.plant2.soilMoisture.at(-1)}</td>
              <td>{data.plants.plant3.soilMoisture.at(-1)}</td>
            </tr>
          </table>
        </div>
      </body>
      <footer className="App-footer">
        <div>
          <br></br>
          <p>
            Made by Celarye using{' '}
            <a className="App-link" href="https://create-react-app.dev/">
              Create React App
            </a>
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
