import { useState, useEffect } from 'react';
import '../styles/Data.css';

interface SensorData {
  Timestamp: string;
  'Soil Moisture 1': string;
  'Soil Moisture 2': string;
  'Soil Moisture 3': string;
  Temperature: string;
  Humidity: string;
}

export default function Data() {
  const [data, setData] = useState<SensorData | null>(null);
  const [timeDifference, setTimeDifference] = useState<number | null>(null);
  const [timestamp, setTimestamp] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch('http://localhost:5000/');
      const stringValue = await response.text();
      const [
        fetchedTimestamp,
        soilMoisture1,
        soilMoisture2,
        soilMoisture3,
        temperature,
        humidity,
      ] = stringValue.split(',');

      setTimestamp(fetchedTimestamp.replace(/[[']+/g, ''));

      const timestampValue = new Date(fetchedTimestamp.replace(/[[']+/g, ''));
      const currentTime = new Date();
      const newTimeDifference =
        currentTime.getTime() - timestampValue.getTime();

      setData({
        Timestamp: fetchedTimestamp.replace(/[[']+/g, ''),
        'Soil Moisture 1': parseFloat(soilMoisture1).toFixed(2),
        'Soil Moisture 2': parseFloat(soilMoisture2).toFixed(2),
        'Soil Moisture 3': parseFloat(
          soilMoisture3.replace(/[\]]+/g, '')
        ).toFixed(3),
        Temperature: parseFloat(temperature).toFixed(2),
        Humidity: parseFloat(humidity).toFixed(2),
      });

      setTimeDifference(newTimeDifference);

      console.log('Data fetched');
    };

    fetchData();
    const interval = setInterval(fetchData, 30000);

    return () => {
      clearInterval(interval);
    };
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      const timestampValue = new Date(timestamp?.replace(/[[']+/g, '') ?? '');
      const currentTime = new Date();
      const newTimeDifference =
        currentTime.getTime() - timestampValue.getTime();
      setTimeDifference(newTimeDifference);
    }, 1000);

    return () => {
      clearInterval(interval);
    };
  }, [timestamp]);

  const formatTimeDifference = (ms: number | null): string | undefined => {
    if (typeof ms === 'number') {
      const minutes = Math.floor(ms / (1000 * 60));
      const seconds = Math.floor((ms % (1000 * 60)) / 1000);
      return `${minutes} minutes ${seconds} seconds`;
    } else {
      console.log('Invalid time difference');
      return timestamp ?? 'Invalid timestamp';
    }
  };

  return (
    <div className="Data">
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
          <h3>Soil Moistures</h3>
          <table>
            <thead>
              <tr>
                <th>Plant 1</th>
                <th>Plant 2</th>
                <th>Plant 3</th>
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
          <p>
            <i>Last Fetched: {formatTimeDifference(timeDifference)} m</i>
          </p>
        </>
      )}
    </div>
  );
}
