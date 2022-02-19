import React, { useState, useRef } from "react";
import logo from "images/Virgin_Group-Logo.wine.svg";
const Nav1 = () => {
  const menuRef = useRef();
  const [menuBtn, setMenuBtn] = useState(false);
  const menuHandler = () => {
    const menu = menuRef.current;
    setMenuBtn(!menuBtn);
    menu.classList.toggle("menu-active");
  };
  return (
    <div className="nav1" id="nav1">
      <div className="nav1_container">
        <div className="nav1_menu" onClick={menuHandler} ref={menuRef}>
          <div className="menu_btn menu_icon">
            <span className="bar"></span>
            <span className="bar"></span>
            <span className="bar"></span>
          </div>
          <div className="menu_btn menu_text">
            {menuBtn ? <span>CLOSE</span> : <span>MENU</span>}
          </div>
          <div className="menu_btn menu_triangle"></div>
        </div>
        <div className="nav_logo">
          <img src={logo} alt="Virgin" />
        </div>
      </div>
      {menuBtn ? <div className="mobile_menu">Home</div> : null}
    </div>
  );
};

export default Nav1;
