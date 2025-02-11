import React from 'react';

const Header = () => {
  return (
    <header className="bg-[#c41e3a] text-white p-4">
      <div className="container mx-auto flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <img 
            src="/assets/logo.png"
            alt="US Observer Logo" 
            className="h-16"
          />
          <h1 className="text-2xl font-bold">
            US Observer Email System
          </h1>
        </div>
      </div>
    </header>
  );
};

export default Header; 