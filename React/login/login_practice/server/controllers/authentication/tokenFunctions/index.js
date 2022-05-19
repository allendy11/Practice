const jwt = require("jsonwebtoken");
require("dotenv").config();
module.exports = {
  generateAccessToken: (userInfo) => {
    return jwt.sign(userInfo, process.env.ACCESS_SECRET, { expiresIn: "1m" });
  },
  generateRefreshToken: (userInfo) => {
    return jwt.sign(userInfo, process.env.REFRESH_SECRET, { expiresIn: "2m" });
  },
  sendAccessToken: (res, accessToken) => {
    res.status(200).send({
      access_token: accessToken,
    });
  },
  sendRefreshToken: (res, refreshToken) => {
    res.cookie("refresh_token", refreshToken, {
      httpOnly: true,
    });
  },
  checkAccessToken: (req) => {
    const authorization = req.headers["authorization"];
    if (!authorization) return null;

    const token = authorization.split(" ")[1];

    try {
      return jwt.verify(token, process.env.ACCESS_SECRET);
    } catch (err) {
      return null;
    }
  },
  checkRefreshToken: (req) => {
    const token = req.cookies("refresh_token");
    try {
      return jwt.verify(token, process.env.REFRESH_SECRET);
    } catch (err) {
      return null;
    }
  },
  clearRefreshToken: (res) => {
    res.clearCookie("refresh_token");
    res.status(200).json({ message: "clear refresh_token" });
  },
};
