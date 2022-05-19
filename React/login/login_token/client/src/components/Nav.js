import React, { useState } from "react";

const Nav = ({ buttonHandler }) => {
  return (
    <div className="nav">
      <div className="nav_container">
        <div className="nav_title">login-practice</div>
        <div className="nav_menu">
          <div
            id="nav_login"
            className="nav_login"
            onClick={(e) => buttonHandler(e)}
          >
            Login
          </div>
        </div>
      </div>
    </div>
  );
};

export default Nav;
