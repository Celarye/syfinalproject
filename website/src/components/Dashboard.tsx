import React, { useEffect, useState, useCallback } from 'react';
import logo from '../includes/logo.png';
import Papa from 'papaparse';
import '../styles/Dashboard.css';

interface SensorData {
  Timestamp: string;
  'Soil Moisture': string;
  Temperature: string;
  Humidity: string;
}

export default function Dashboard() {
  const [csvData, setCsvData] = useState<SensorData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  const findLastNonEmptyLineIndex = useCallback(
    (data: SensorData[]): number => {
      let lastIndex = data.length - 1;
      while (
        lastIndex >= 0 &&
        Object.values(data[lastIndex]).every(
          (value) => typeof value === 'string' && !value.trim()
        )
      ) {
        lastIndex--;
      }
      return lastIndex;
    },
    []
  );

  useEffect(() => {
    const formatDate = (date: Date): string => {
      const day = padNumber(date.getDate());
      const month = padNumber(date.getMonth() + 1);
      const year = date.getFullYear();
      return `${day}-${month}-${year}`;
    };

    const padNumber = (num: number): string => {
      return num.toString().padStart(2, '0');
    };

    const fetchData = async () => {
      const currentDate = new Date();
      const formattedDate = formatDate(currentDate);

      const filePath = `http://localhost:5000/data/sensorsData_${formattedDate}.csv`;
      const response = await fetch(filePath);
      const reader = response.body?.getReader();
      const result = await reader?.read(); // raw array
      const decoder = new TextDecoder('utf-8');
      const csv = decoder.decode(result?.value); // the csv text
      const parsedData: SensorData[] = Papa.parse(csv, { header: true })
        .data as SensorData[];
      const lastNonEmptyLineIndex = findLastNonEmptyLineIndex(parsedData);
      console.log(parsedData);

      if (lastNonEmptyLineIndex !== -1) {
        const lastItem = parsedData[lastNonEmptyLineIndex];
        setCsvData(lastItem as SensorData);
      } else {
        setCsvData(null);
      }

      setLoading(false);
    };

    fetchData();
    const interval = setInterval(fetchData, 60000);

    return () => {
      clearInterval(interval);
    };
  }, [findLastNonEmptyLineIndex]);

  return (
    <div className="dashboard">
      <img src={logo} className="dashboard-logo App-logo" alt="logo" />
      <div>
        {loading ? (
          <div>Loading...</div>
        ) : csvData ? (
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
                  <td>{csvData.Temperature}</td>
                  <td>{csvData['Soil Moisture']}</td>
                  <td>{csvData.Humidity}</td>
                </tr>
              </tbody>
            </table>
            <p className="dashboard-fetch-date">
              <i>Last Fetched: {csvData.Timestamp}</i>
            </p>
          </>
        ) : (
          <div>No data fetched or available</div>
        )}
      </div>
    </div>
  );
}
