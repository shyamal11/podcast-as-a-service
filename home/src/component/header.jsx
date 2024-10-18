import React from 'react';
import '../static/css/header.css'; // Import the CSS file for styling

const Header = () => {
  return (
    <header className="header">
      <div className="logo">
        <img src="path-to-your-logo.png" alt="Logo" className="logo-img" />
      </div>

      <div className="search-bar">
        <input type="text" placeholder="Search..." />
      </div>

      <div className="login">
        <a href="/login">Login</a>
      </div>
    </header>
  );
}

export default Header;
