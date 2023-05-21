import { useEffect, useState } from 'react';
import Papa from 'papaparse';
import logo from '../includes/logo.png';
import '../styles/Dashboard.css';

interface SensorData {
  Timestamp: string;
  SoilMoisture: number;
  Temperature: number;
  Humidity: number;
}

export default function Dashboard() {
  const [csvData, setCsvData] = useState<SensorData[]>([]);

  const fetchDataFromCSV = () => {
    const currentDate = new Date().toLocaleDateString('en-US', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
    });

    const filePath = `../data/sensorsData_${currentDate}.csv`;

    fetch(filePath)
      .then((response) => response.text())
      .then((fileData) => {
        // Parse the CSV data
        const { data } = Papa.parse(fileData, { header: true });

        setCsvData(data as SensorData[]);
      })
      .catch((error) => {
        console.error(error);
      });
  };

  useEffect(() => {
    fetchDataFromCSV();

    const interval = setInterval(fetchDataFromCSV, 60000);

    return () => {
      clearInterval(interval);
    };
  }, []);

  return (
    <div className="dashboard">
      <img src={logo} className="dashboard-logo App-logo" alt="logo" />
      <div>
        {csvData.length > 0 ? (
          <table>
            <thead>
              <tr>
                <th>Temperature</th>
                <th>Soil Moisture</th>
                <th>Humidity</th>
              </tr>
            </thead>
            <tbody>
              {csvData.map((row, index) => (
                <tr key={index}>
                  <td>{row.Temperature}</td>
                  <td>{row.SoilMoisture}</td>
                  <td>{row.Humidity}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div>No data available</div>
        )}
        <p className="dashboard-fetch-date">
          <i>
            Last Fetched:{' '}
            {csvData.length > 0 ? csvData[csvData.length - 1].Timestamp : ''}
          </i>
        </p>
      </div>
    </div>
  );
}
