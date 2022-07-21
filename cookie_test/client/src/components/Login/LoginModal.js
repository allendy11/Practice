import React, { useState } from "react";
import "./LoginModal.css";
import axios from "axios";

const LoginModal = ({ isLogin, setIsLogin }) => {
  const [userInput, setUserInput] = useState({
    id: "",
    password: "",
  });
  const handleChange = (e) => {
    if (e.target.id === "id") {
      setUserInput({
        ...userInput,
        id: e.target.value,
      });
    } else if (e.target.id === "password") {
      setUserInput({
        ...userInput,
        password: e.target.value,
      });
    }
  };
  const handleClick = (e) => {
    console.log(userInput);
    axios({
      method: "POST",
      url: "http://localhost:4000/user/login",
      data: {
        id: userInput.id,
        password: userInput.password,
      },
      withCredentials: true,
    }).then((res) => {
      console.log(res.data);
      setIsLogin(true);
    });
  };
  return (
    <div id="LoginModal">
      <div className="loginModal-container">
        <input
          id="id"
          type="text"
          placeholder="test"
          onChange={(e) => handleChange(e)}
        />
        <input
          id="password"
          type="text"
          placeholder="1234"
          onChange={(e) => handleChange(e)}
        />
        <button onClick={(e) => handleClick(e)}>LOGIN</button>
      </div>
    </div>
  );
};

export default LoginModal;
