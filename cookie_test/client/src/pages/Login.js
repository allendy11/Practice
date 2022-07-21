import React from "react";
import LoginModal from "../components/Login/LoginModal";
import "./Login.css";
const Login = ({ isLogin, setIsLogin }) => {
  return (
    <div id="Login">
      {isLogin ? (
        <div>로그인 성공</div>
      ) : (
        <LoginModal isLogin={isLogin} setIsLogin={setIsLogin} />
      )}
    </div>
  );
};

export default Login;
