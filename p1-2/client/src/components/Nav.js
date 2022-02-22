import React from "react";

const Nav = () => {
  return (
    <div className="nav" id="nav">
      <div className="nav_container">
        <div className="nav_title">
          <a href="#home">COLOR</a>
        </div>
        <div className="mobile_menu">
          <span className="bar"></span>
          <span className="bar"></span>
          <span className="bar"></span>
        </div>
        <ul className="nav_menu">
          <li className="nav_item">
            <a href="#home">Home</a>
          </li>
          <li className="nav_item">
            <a href="#about">About</a>
          </li>
          <li className="nav_item">
            <a href="#services">Services</a>
          </li>
          <li className="nav_item">
            <a href="#signup">Sign Up</a>
          </li>
        </ul>
      </div>
    </div>
  );
};

export default Nav;
