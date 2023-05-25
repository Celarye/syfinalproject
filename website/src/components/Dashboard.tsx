import { useState, useEffect } from 'react';
import logo from '../includes/logo.png';
import '../styles/Dashboard.css';

interface SensorData {
  Timestamp: string;
  'Soil Moisture 1': string;
  'Soil Moisture 2': string;
  'Soil Moisture 3': string;
  Temperature: string;
  Humidity: string;
}

export default function Dashboard() {
  const [data, setData] = useState<SensorData | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch('http://localhost:5000/');
      const stringValue = await response.text();
      const [
        timestamp,
        soilMoisture1,
        soilMoisture2,
        soilMoisture3,
        temperature,
        humidity,
      ] = stringValue.split(',');
      setData({
        Timestamp: timestamp.replace(/[[]+/g, ''),
        'Soil Moisture 1': parseFloat(soilMoisture1).toFixed(3),
        'Soil Moisture 2': parseFloat(soilMoisture2).toFixed(3),
        'Soil Moisture 3': parseFloat(
          soilMoisture3.replace(/[\]]+/g, '')
        ).toFixed(3),
        Temperature: parseFloat(temperature).toFixed(3),
        Humidity: parseFloat(humidity).toFixed(3),
      });
      console.log('Data fetched');
    };

    fetchData();
    const interval = setInterval(fetchData, 30000);

    return () => {
      clearInterval(interval);
    };
  }, []);

  return (
    <div className="dashboard">
      <img src={logo} className="dashboard-logo App-logo" alt="logo" />
      <div>
        {!data ? (
          <div>No Data Fetched Yet...</div>
        ) : (
          <>
            <table>
              <thead>
                <tr>
                  <th>Temperature</th>
                  <th>Humidity</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>{data.Temperature}°C</td>
                  <td>{data.Humidity}%</td>
                </tr>
              </tbody>
            </table>
            <table>
              <thead>
                <tr>
                  <th>Soil Moisture 1</th>
                  <th>Soil Moisture 2</th>
                  <th>Soil Moisture 3</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>{data['Soil Moisture 1']}%</td>
                  <td>{data['Soil Moisture 2']}%</td>
                  <td>{data['Soil Moisture 3']}%</td>
                </tr>
              </tbody>
            </table>

            <p className="dashboard-fetch-date">
              <i>Last Fetched: {data.Timestamp}</i>
            </p>
          </>
        )}
      </div>
    </div>
  );
}
