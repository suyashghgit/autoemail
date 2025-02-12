import React from 'react';

const Header = ({ onLogout }) => {
  return (
    <header className="fixed top-0 left-0 right-0 bg-white shadow-md z-50">
      <div className="container mx-auto px-6 py-4 flex justify-between items-center">
        <h1 className="text-2xl font-bold text-[#c41e3a]">US Observer Email System</h1>
        <button
          onClick={onLogout}
          className="bg-[#c41e3a] text-white px-4 py-2 rounded hover:bg-red-700"
        >
          Logout
        </button>
      </div>
    </header>
  );
};

export default Header; 