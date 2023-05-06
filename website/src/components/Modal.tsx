import logo from '../includes/logo.png';
import '../styles/App.css';
import '../styles/Modal.css';

type ModalProps = {
  onClose: () => void;
};

export default function Modal(props: ModalProps) {
  function modalClose() {
    props.onClose();
  }
  return (
    <div className="Modal">
      <img src={logo} className="Modal-logo App-logo" alt="logo" />
      <h1 className="Modal-title">House Plants Manager</h1>
      <p className="Modal-description">
        Modernize your house plant management!
      </p>
      <div className="Modal-features">
        <div className="Modal-features-column">
          <h3 className="Modal-features-title">Monitoring</h3>
          <p>
            Effortlessly monitor the health of your plants with a user-friendly
            system
          </p>
        </div>
        <div className="Modal-features-column Modal-features-column2">
          <h3 className="Modal-features-title">Automation</h3>
          <p>
            Enable automatic responses on the website based on the conditions of
            your plant
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
      <button className="Modal-button" type="button" onClick={modalClose}>
        Understood!
      </button>
    </div>
  );
}
