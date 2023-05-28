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
  const [showDataExample, setShowDataExample] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      const appUrl = localStorage.getItem('appUrl');
      if (appUrl) {
        const response = await fetch(appUrl);
        const stringValue = await response.text();
        const cleanStringValue = stringValue.replace(/\['|'/g, '');
        const [
          fetchedTimestamp,
          soilMoisture1,
          soilMoisture2,
          soilMoisture3,
          temperature,
          humidity,
        ] = cleanStringValue.split(',');

        setData({
          Timestamp: fetchedTimestamp.replace(
            /(\d{2})-(\d{2})-(\d{4}) (\d{2}):(\d{2}):(\d{2})/,
            '$3-$2-$1T$4:$5:$6'
          ),
          'Soil Moisture 1': parseFloat(soilMoisture1).toFixed(2),
          'Soil Moisture 2': parseFloat(soilMoisture2).toFixed(2),
          'Soil Moisture 3': parseFloat(soilMoisture3).toFixed(2),
          Temperature: parseFloat(temperature).toFixed(2),
          Humidity: parseFloat(humidity).toFixed(2),
        });
        console.log('Data fetched');
      }
    };

    fetchData();

    const interval = setInterval(fetchData, 6000);

    return () => {
      clearInterval(interval);
    };
  }, []);

  useEffect(() => {
    const updateTimestampDifference = () => {
      const timestampValue = new Date(data?.Timestamp ?? '');
      const currentTime = new Date();

      if (!isNaN(timestampValue.getTime())) {
        const newTimeDifference =
          currentTime.getTime() - timestampValue.getTime();
        setTimeDifference(newTimeDifference);
      } else {
        console.log('Invalid timestamp');
        setTimeDifference(null);
      }
    };

    updateTimestampDifference();

    const interval = setInterval(updateTimestampDifference, 60000);

    return () => {
      clearInterval(interval);
    };
  }, [data?.Timestamp]);

  const formatTimeDifference = (ms: number | null): string | undefined => {
    if (typeof ms === 'number' && !isNaN(ms)) {
      const minutes = Math.floor(ms / (1000 * 60));
      return `${minutes} minute(s) ago`;
    } else {
      console.log('Invalid time difference');
      return data?.Timestamp.replace('T', ' ') ?? 'Invalid timestamp';
    }
  };

  function toggleDataExample() {
    setShowDataExample(!showDataExample);
  }

  return (
    <div className="Data">
      {!data ? (
        <>
          <h1 className="Data-negative-title">No Data Fetched Yet...</h1>
          <p className="Data-negative-paragrapgh">
            Make sure your set URL{' '}
            <code className="App-code-block">
              ({localStorage.getItem('appUrl') ?? 'No URL defined'})
            </code>{' '}
            is correct and that the sensors script is running on your Raspberry
            Pi.
            <br />
            You can update your set URL through the info modal (can be opened
            with the info button).
          </p>
          <button
            className="App-button Data-negative-example-button"
            type="button"
            onClick={toggleDataExample}
          >
            Data Example
          </button>
          {showDataExample && (
            <div className="Data-example">
              <h1 className="Data-title">Data Example</h1>
              <h3 className="Data-title">Global values</h3>
              <table className="Data-table">
                <thead>
                  <tr>
                    <th className="Data-table-column Data-table-row">
                      Temperature
                    </th>
                    <th className="Data-table-row">Humidity</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td className="Data-table-column">Temperature Value</td>
                    <td>Humidity Value</td>
                  </tr>
                </tbody>
              </table>
              <h3 className="Data-title">Soil Moistures</h3>
              <table className="Data-table">
                <thead className="Data-table-row">
                  <tr>
                    <th className="Data-table-row">Plant 1</th>
                    <th className="Data-table2-column Data-table-row">
                      Plant 2
                    </th>
                    <th className="Data-table-row">Plant 3</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>Plant 1 Value</td>
                    <td className="Data-table2-column">Plant 2 Value</td>
                    <td>Plant 3 Value</td>
                  </tr>
                </tbody>
              </table>
              <p className="Data-last-fetched">
                <i>Last Fetched: Fetch Time</i>
              </p>
              <button
                className="App-button"
                type="button"
                onClick={toggleDataExample}
              >
                Close
              </button>
            </div>
          )}
        </>
      ) : (
        <>
          <h3 className="Data-title">Global values</h3>
          <table className="Data-table">
            <thead>
              <tr>
                <th className="Data-table-column Data-table-row">
                  Temperature
                </th>
                <th className="Data-table-row">Humidity</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td className="Data-table-column">{data.Temperature}°C</td>
                <td>{data.Humidity}%</td>
              </tr>
            </tbody>
          </table>
          <h3 className="Data-title">Soil Moistures</h3>
          <table className="Data-table">
            <thead className="Data-table-row">
              <tr>
                <th className="Data-table-row">Plant 1</th>
                <th className="Data-table2-column Data-table-row">Plant 2</th>
                <th className="Data-table-row">Plant 3</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>{data['Soil Moisture 1']}%</td>
                <td className="Data-table2-column">
                  {data['Soil Moisture 2']}%
                </td>
                <td>{data['Soil Moisture 3']}%</td>
              </tr>
            </tbody>
          </table>
          <p className="Data-last-fetched">
            <i>Last Fetched: {formatTimeDifference(timeDifference)}</i>
          </p>
        </>
      )}
    </div>
  );
}
