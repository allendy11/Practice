import React from "react";
import "./App.css";
import Nav from "components/Nav";
import Home from "pages/Home";
import About from "pages/About";
import Services from "pages/Services";
import Join from "pages/Join";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
function App() {
  return (
    <div className="App">
      <Router>
        <Nav />
        <Routes>
          <Route path="/" element={<Home />}>
            <Route path="#about" element={<About />} />
            <Route path="#services" element={<Services />} />
          </Route>
        </Routes>
        {/* <Home/> */}
        {/* <Router>
        <Nav />
        <Routes>
        <Route path='/' element={<Home/>}/>
        <Route path='/about' element={<About/>}/>
        </Routes>
      </Router> */}
      </Router>
    </div>
  );
}

export default App;
