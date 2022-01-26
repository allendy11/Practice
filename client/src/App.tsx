import React from 'react';
import './App.css';
import Nav from 'components/Nav'
import Home from 'pages/Home'
import About from 'pages/About'
import Service from 'pages/Service'
import Join from 'pages/Join'

function App() {
  return (
    <div className="App">
      <div className='Nav'>
        <Nav />
      </div>
      <div className='Pages'>
        <Home />
        <About />
        <Service />
        <Join />
      </div>
    </div>
  );
}

export default App;
