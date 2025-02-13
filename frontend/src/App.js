import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import Dashboard from './components/Dashboard';
import Login from './components/Login';
import { Toaster } from 'react-hot-toast';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    // Check if user is already authenticated
    const authStatus = localStorage.getItem('isAuthenticated');
    if (authStatus === 'true') {
      setIsAuthenticated(true);
    }
  }, []);

  const handleLogin = () => {
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    localStorage.removeItem('isAuthenticated');
    setIsAuthenticated(false);
  };

  return (
    <>
      <Toaster />
      {!isAuthenticated ? (
        <Login onLogin={handleLogin} />
      ) : (
        <div className="min-h-screen bg-gray-100">
          <Header onLogout={handleLogout} />
          <Dashboard />
        </div>
      )}
    </>
  );
}

export default App; 