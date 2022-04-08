const { User } = require("../../models");
const {
  generateAccessToken,
  generateRefreshToken,
  sendAccessToken,
  sendRefreshToken,
  checkAccessToken,
  checkRefreshToken,
} = require("./tokenFunctions");

module.exports = (req, res) => {
  const { email, password, username } = req.body;
  User.create({
    email,
    password,
    username,
  }).then(() => {
    generateAccessToken();
    generateRefreshToken();
    sendAccessToken();
    sendRefreshToken();
  });
};
