import { useState, useEffect } from 'react';
import { ModalProps } from './App';
import logo from '../includes/logo.png';
import '../styles/Modal.css';

export default function Modal(props: ModalProps) {
  const [urlInput, setUrlInput] = useState('');
  const [isValidUrl, setIsValidUrl] = useState(false);
  const [isConnectClicked, setIsConnectClicked] = useState(false);
  const [showMessage, setShowMessage] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    const storedUrl = localStorage.getItem('appUrl');
    if (storedUrl) {
      setUrlInput(storedUrl);
      setIsValidUrl(isUrlValid(storedUrl));
      setIsConnectClicked(true);
    }
  }, []);

  function modalClose() {
    if (urlInput === '' || !isValidUrl || !isConnectClicked) {
      return;
    }
    props?.onClose?.();
  }

  function handleUrlInputChange(event: React.ChangeEvent<HTMLInputElement>) {
    const inputValue = event.target.value;
    setUrlInput(inputValue);
    setIsValidUrl(isUrlValid(inputValue));
  }

  function handleConnectButtonClick() {
    if (!isUrlValid(urlInput)) {
      setMessage('Invalid URL. Please try again.');
      setShowMessage(true);
      return;
    }
    localStorage.setItem('appUrl', urlInput);
    setIsConnectClicked(true);
    setMessage('URL saved successfully!');
    setShowMessage(true);
  }

  function isUrlValid(url: string) {
    const validUrlPattern =
      /^(https?:\/\/)(localhost|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(:\d{1,5})(\/)?$/i;
    return validUrlPattern.test(url);
  }

  return (
    <>
      <div className={`Modal-overlay${props.isShowing ? 'Show' : ''}`}></div>
      <div className="Modal">
        <img src={logo} className="Modal-logo" alt="logo" />
        <h1 className="Modal-title">House Plants Manager</h1>
        <p className="Modal-description">
          Modernize your house plant management!
        </p>
        <div className="Modal-features">
          <div className="Modal-features-column">
            <h3 className="Modal-features-title">Monitoring</h3>
            <p>
              Effortlessly monitor the health of your plants with a
              user-friendly system
            </p>
          </div>
          <div className="Modal-features-column Modal-features-column2">
            <h3 className="Modal-features-title">Automation</h3>
            <p>
              Enable automatic responses on the website based on the conditions
              of your plant
            </p>
          </div>
          <div className="Modal-features-column">
            <h3 className="Modal-features-title">Notifications</h3>
            <p>
              Stay informed about the condition and care of your plants with
              timely notifications
            </p>
          </div>
        </div>
        <div className="Modal-usage">
          <h3 className="Modal-usage-title">App Usage</h3>
          <p className="Modal-usage-paragraph">
            To use this app and have it display data, you will need to run the
            sensors script on a Raspberry Pi and connect the app to it. To do
            this, clone the repository{' '}
            <code className="App-code-block">
              https://github.com/Celarye/syfinalproject
            </code>{' '}
            and in the main directory, run{' '}
            <code className="App-code-block">cd sensors</code> and{' '}
            <code className="App-code-block">bash sensorsStartup.sh</code>.
            After this, a URL will appear in the console. Place this URL in the
            input field below.
          </p>
          <span>
            <div className="Modal-url-input">
              <input
                className="Modal-url-input-field"
                type="url"
                placeholder="URL"
                value={urlInput}
                onChange={handleUrlInputChange}
              ></input>
              {showMessage && <p className="Modal-url-validation">{message}</p>}
            </div>
            <button
              className="App-button Modal-url-button"
              type="button"
              onClick={handleConnectButtonClick}
            >
              Connect
            </button>
          </span>
        </div>
        <button
          className="Modal-close-button"
          type="button"
          onClick={modalClose}
        >
          &times;
        </button>
      </div>
    </>
  );
}
