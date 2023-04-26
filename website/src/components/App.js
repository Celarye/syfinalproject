import data from '../data/data.json';
import '../styles/main.css';

console.log(data);

function App() {
  return (
    <div className="App">
      <body className="App-body">
        <div>
          <p>
            <i>Last Fetched: {data.creationDate}</i>
          </p>
          <h>
            <b>Global Values</b>
          </h>
          <p>Temperature: {data.global.temp.at(-1)}</p>
          <h>
            <b className="App-body-title">
              Plant Specific Soil Moisture Values
            </b>
          </h>
          <div className="App-body-row1">
            <div className="App-body-column">
              <div className="App-body-row2">
                <h>Plant 1</h>
              </div>
              <div className="App-body-row3">
                <p>{data.plants.plant1.soilMoisture.at(-1)}</p>
              </div>
            </div>
            <div className="App-body-column">
              <div className="App-body-row2">
                <h>Plant 2</h>
              </div>
              <div className="App-body-row3">
                <p>{data.plants.plant2.soilMoisture.at(-1)}</p>
              </div>
            </div>
            <div className="App-body-column">
              <div className="App-body-row2">
                <h>Plant 3</h>
              </div>
              <div className="App-body-row3">
                <p>{data.plants.plant3.soilMoisture.at(-1)}</p>
              </div>
            </div>
          </div>
        </div>
      </body>
      <footer className="App-footer">
        <div>
          <p>
            Made by Celarye Using{' '}
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
