import logo from "./logo.svg";
import "./App.css";
import React, { useState } from "react";
import Nav from "./components/Nav";
import Loginpage from "./pages/Loginpage";

function App() {
  const [loginOn, setLoginOn] = useState(false);
  const buttonHandler = (e) => {
    if (e.target.id === "nav_login") {
      setLoginOn(true);
    } else if (e.target.id === "close") {
      setLoginOn(false);
    }
  };
  return (
    <div className="App">
      <Nav
        loginOn={loginOn}
        setLoginOn={setLoginOn}
        buttonHandler={buttonHandler}
      />
      {loginOn ? <Loginpage buttonHandler={buttonHandler} /> : null}
    </div>
  );
}

export default App;
