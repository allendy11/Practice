import React from "react";

const Loginpage = ({ buttonHandler }) => {
  return (
    <div className="loginpage">
      <div
        id="close"
        className="button_close"
        onClick={(e) => buttonHandler(e)}
      >
        X
      </div>
      <div className="login_modal">
        <div className="input_box">
          <span>Email</span>
          <input type="text" />
        </div>
        <div className="input_box">
          <span>Password</span>
          <input type="text" />
        </div>
        <div className="button_box">
          <div className="button_login">
            <span>Login</span>
          </div>
          <div className="button_signup">
            <span>Sign-up</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Loginpage;
