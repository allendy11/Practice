import React from "react";
import { Link } from "react-router-dom";
const Nav = () => {
  return (
    <nav className="nav">
      <div className="nav-container">
        <a href="#home" className="nav-title">
          COLOR
        </a>
        <div id="mobile-menu">
          <span className="menu-icon"></span>
          <span className="menu-icon"></span>
          <span className="menu-icon"></span>
        </div>
        <ul className="nav-menu-box">
          <li className="nav-menu" id="home-btn">
            <a href="#home">Home</a>
          </li>
          <li className="nav-menu" id="about-btn">
            <a href="#about">About</a>
          </li>
          <li className="nav-menu" id="services-btn">
            <a href="#services">Services</a>
          </li>
          <li className="nav-menu" id="join-btn">
            <a href="#join">Sign up</a>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Nav;
