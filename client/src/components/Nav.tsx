import React from "react";
import { Link } from "react-router-dom";
const Nav = () => {
  return (
    <nav className="navbar">
      <div className="navbar__container">
        <a href="#home" id="navbar__logo">
          COLOR
        </a>
        <div className="navbar__toggle" id="mobile-menu">
          <span className="bar"></span> <span className="bar"></span>
          <span className="bar"></span>
        </div>
        <ul className="navbar__menu">
          <li className="navbar__item">
            {/* <a href="#home" className="navbar__links" id="home-page">Home</a> */}
            <Link to="/">Home</Link>
          </li>
          <li className="navbar__item">
            <a href="#about" className="navbar__links" id="about-page">
              About
            </a>
          </li>
          <li className="navbar__item">
            <a href="#services" className="navbar__links" id="services-page">
              Services
            </a>
          </li>
          <li className="navbar__btn">
            <a href="#sign-up" className="button" id="signup">
              Sign Up
            </a>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Nav;
