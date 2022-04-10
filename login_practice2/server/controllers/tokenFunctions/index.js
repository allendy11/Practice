const { sign, verify } = require("jsonwebtoken");
require("dotenv").config();

module.exports = {
  generateAccessToken: (data) => {
    return sign(data, process.env.ACCESS_SECRET, { expiresIn: "1m" });
  },
  generateRefreshToken: (data) => {
    return sign(data, process.env.REFRESH_SECRET, { expiresIn: "3m" });
  },
  checkAccessToken: (req) => {
    const token = req.headers["authorization"].split(" ")[1];
    const data = verify(token, process.env.ACCESS_SECRET);
    if (!data) {
      return null;
    } else {
      return data;
    }
  },
};
