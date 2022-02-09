import React from "react";

const Nav = () => {
  return (
    <div className="nav">
      <div className="nav-container">
        <a href="#home" className="nav-logo">
          COLOR
        </a>
        <div className="mobile-menu">
          <span className="bar"></span>
          <span className="bar"></span>
          <span className="bar"></span>
        </div>
        <ul className="nav-menu">
          <li className="nav-item">
            <a href="#home" className="nav-link">
              Home
            </a>
          </li>
          <li className="nav-item">
            <a href="#about" className="nav-link">
              About
            </a>
          </li>
          <li className="nav-item">
            <a href="services" className="nav-link">
              Services
            </a>
          </li>
          <li className="nav-item">
            <a href="signup" className="nav-link">
              Sign Up
            </a>
          </li>
        </ul>
      </div>
    </div>
  );
};

export default Nav;
