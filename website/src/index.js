import React from 'react';
import ReactDOM from 'react-dom/client';
import Navbar from './components/Navbar';
import Dashboard from './components/Dashboard';
import Footer from './components/Footer';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Navbar />
    <Dashboard />
    <Footer />
  </React.StrictMode>,
);
