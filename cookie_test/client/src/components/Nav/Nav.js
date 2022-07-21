import React from "react";
import { Link } from "react-router-dom";
import "./Nav.css";
const Nav = ({ isLogin, setIsLogin }) => {
  const handleClick = (e) => {
    setIsLogin(false);
  };
  return (
    <div id="Nav">
      <div className="nav-container">
        <Link to="/">
          <div className="nav-box">TITLE</div>
        </Link>
        {isLogin ? (
          <div style={{ cursor: "pointer" }} onClick={(e) => handleClick(e)}>
            LOGOUT
          </div>
        ) : (
          <Link to="/login">
            <div className="nav-box">LOGIN</div>
          </Link>
        )}
        <Link to="/mypage">
          <div className="nav-box">MYPAGE</div>
        </Link>
      </div>
    </div>
  );
};

export default Nav;
