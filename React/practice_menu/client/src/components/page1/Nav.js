import React, { useState, useRef } from "react";

const Nav = () => {
  const [currentMenu, setCurrentMenu] = useState("");
  const menuRef = useRef();
  const menuHandler = () => {
    menuRef.current.classList.toggle("p1_menu_active");
  };
  const menuEnter = (e) => {
    setCurrentMenu(e.target.id);
  };
  const menuOut = () => {
    setCurrentMenu("");
  };
  return (
    <div className="p1_nav">
      <div className="p1_nav_container" ref={menuRef}>
        <div className="p1_btn_menu" onClick={menuHandler}>
          MENU
        </div>
        <div className="p1_mobile_menu">
          <div className="p1_menu_box">
            <ul className="p1_menu_items">
              <li
                id="1"
                onMouseEnter={(e) => menuEnter(e)}
                onMouseLeave={menuOut}
              >
                menu1
              </li>
              <li
                id="2"
                onMouseEnter={(e) => menuEnter(e)}
                onMouseLeave={menuOut}
              >
                menu2
              </li>
              <li
                id="3"
                onMouseEnter={(e) => menuEnter(e)}
                onMouseLeave={menuOut}
              >
                menu3
              </li>
              <li
                id="4"
                onMouseEnter={(e) => menuEnter(e)}
                onMouseLeave={menuOut}
              >
                menu4
              </li>
              <li
                id="5"
                onMouseEnter={(e) => menuEnter(e)}
                onMouseLeave={menuOut}
              >
                menu5
              </li>
            </ul>
          </div>
          <div className="p1_menu_box">
            {currentMenu === "1" ? (
              <ul className="p1_menu_items2">
                <li>menu1_1</li>
                <li>menu1_2</li>
                <li>menu1_3</li>
              </ul>
            ) : currentMenu === "2" ? (
              <ul className="p1_menu_items2">
                <li>menu2_1</li>
                <li>menu2_2</li>
              </ul>
            ) : currentMenu === "3" ? (
              <ul className="p1_menu_items2">
                <li>menu3_1</li>
              </ul>
            ) : currentMenu === "4" ? (
              <ul className="p1_menu_items2">
                <li>menu4_1</li>
                <li>menu4_2</li>
                <li>menu4_3</li>
                <li>menu4_4</li>
              </ul>
            ) : null}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Nav;
