import React from 'react'
import {Link} from 'react-router-dom'
const Nav = () => {
  return (
    <div className='nav-container'>
      <div className='nav-r'>
        <div className='nav-title'>
          TITLE
        </div>
      </div>
      <div className='nav-l'>
        <div className='nav-pages nav-home'>Home</div>
        <div className='nav-pages nav-about'>AboutUs</div>
        <div className='nav-pages nav-service'>Service</div>
        <div className='nav-pages nav-join'>Join</div>
      </div>
    
    </div>
  )
}

export default Nav
