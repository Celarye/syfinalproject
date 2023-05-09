import data from '../data/data.json';
import logo from '../includes/logo.png';
import '../styles/Dashboard.css';

export default function Dashboard() {
  return (
    <>
      <div className="dashboard">
        <div>
          <img src={logo} className="dashboard-logo App-logo" alt="logo" />
          <h2 className="dashboard-title1">
            <b>Global Values</b>
          </h2>
          <p>Temperature: {data.global.temp.at(-1)}</p>
          <p>Humidity: {data.global.humidity.at(-1)}</p>
          <h2 className="dashboard-title2">
            <b>Plant Specific Soil Moisture Values</b>
          </h2>
          <div className="dashboard-row">
            <div className="dashboard-column">
              <div className="dashboard-row1">
                <h3>Plant 1</h3>
              </div>
              <div className="dashboard-row2">
                <p>{data.plants.plant1.soilMoisture.at(-1)}</p>
              </div>
            </div>
            <div className="dashboard-column">
              <div className="dashboard-row1 dashboard-column-center">
                <h3>Plant 2</h3>
              </div>
              <div className="dashboard-row2 dashboard-column-center">
                <p>{data.plants.plant2.soilMoisture.at(-1)}</p>
              </div>
            </div>
            <div className="dashboard-column">
              <div className="dashboard-row1">
                <h3>Plant 3</h3>
              </div>
              <div className="dashboard-row2">
                <p>{data.plants.plant3.soilMoisture.at(-1)}</p>
              </div>
            </div>
          </div>
          <p className="dashboard-fetch-date">
            <i>Last Fetched: {new Date(Date.now()).toLocaleString('nl-BE')}</i>
          </p>
        </div>
      </div>
    </>
  );
}
