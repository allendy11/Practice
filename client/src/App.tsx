import React from "react";
import "./App.css";
import Nav from "components/Nav";
import Home from "pages/Home";
import About from "pages/About";
import Services from "pages/Services";
import Join from "pages/Join";
function App() {
  return (
    <div className="App">
      <Nav />
      <Home />
      <About />
      <Services />
      <Join />
    </div>
  );
}

export default App;
