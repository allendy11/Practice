import React from "react";
import { Link } from "react-router-dom";
import "./css/Nav.css";
const Nav = () => {
  return (
    <div id="Nav">
      <div className="nav-container">
        <Link to="/">
          <div className="nav-title">TITLE</div>
        </Link>
      </div>
    </div>
  );
};

export default Nav;
