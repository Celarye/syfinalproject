import React, { useState, useEffect } from 'react';
import logo from '../includes/logo.png';
import '../styles/Dashboard.css';

interface SensorData {
  Timestamp: string;
  'Soil Moisture': string;
  Temperature: string;
  Humidity: string;
}

export default function Dashboard() {
  const [data, setData] = useState<SensorData | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch('http://localhost:5000/');
      const stringValue = await response.text();
      const [timestamp, soilMoisture, temperature, humidity] =
        stringValue.split(',');
      setData({
        Timestamp: timestamp,
        'Soil Moisture': soilMoisture,
        Temperature: temperature,
        Humidity: humidity,
      });
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
          <div>Loading...</div>
        ) : (
          <>
            <table>
              <thead>
                <tr>
                  <th>Temperature</th>
                  <th>Soil Moisture</th>
                  <th>Humidity</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>{data.Temperature}</td>
                  <td>{data['Soil Moisture']}</td>
                  <td>{data.Humidity}</td>
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
