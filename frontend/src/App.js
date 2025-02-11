import React from 'react';
import Header from './components/Header';
import Dashboard from './components/Dashboard';
import { Toaster } from 'react-hot-toast';

function App() {
  return (
    <>
      <Toaster />
      <div className="min-h-screen bg-gray-100">
        <Header />
        <Dashboard />
      </div>
    </>
  );
}

export default App; 