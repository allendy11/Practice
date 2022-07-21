import React, { useState, useEffect } from "react";
import axios from "axios";

const Mypage = ({ isLogin, setIsLogin }) => {
  const [userInfo, setUserInfo] = useState({
    name: "",
    email: "",
    mobile: "",
  });
  useEffect(() => {
    console.log("a");
    axios({
      method: "GET",
      url: "http://localhost:4000/user/mypage",
      withCredentials: true,
    }).then((res) => {
      console.log(res.data);
      setUserInfo({
        name: res.data.name,
        email: res.data.email,
        mobile: res.data.mobile,
      });
    });
  }, []);
  return (
    <div>
      {isLogin ? (
        <div>
          <div>
            <span style={{ margin: "0 1rem" }}>name : </span>
            <span>{userInfo.name}</span>
          </div>
          <div>
            <span style={{ margin: "0 1rem" }}>email :</span>
            <span>{userInfo.email}</span>
          </div>
          <div>
            <span style={{ margin: "0 1rem" }}>mobile :</span>
            <span>{userInfo.mobile}</span>
          </div>
        </div>
      ) : (
        <div>로그인 하세요</div>
      )}
    </div>
  );
};

export default Mypage;
