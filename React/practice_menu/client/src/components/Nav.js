import React from "react";
import { Link } from "react-router-dom";
const Nav = () => {
  return (
    <nav className="nav">
      <div className="nav_container">
        <div className="home">
          <Link to="/">Home</Link>
        </div>
        <div className="nav_menu">
          <Link to="/page1">Page1</Link>
        </div>
      </div>
    </nav>
  );
};

export default Nav;
