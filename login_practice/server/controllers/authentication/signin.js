const { User } = require("../../models");
const {
  generateAccessToken,
  generateRefreshToken,
  sendAccessToken,
  sendRefreshToken,
} = require("./tokenFunctions");

module.exports = (req, res) => {
  User.findOne({
    where: {
      email: req.body.email,
      password: req.body.password,
    },
    attributes: ["id", "email", "username"],
  }).then((userInfo) => {
    if (!userInfo) {
      return res.status(404).json({ message: "user is not found" });
    }
    const access_token = generateAccessToken({
      id: userInfo.id,
      email: userInfo.email,
      username: userInfo.username,
    });
    const refresh_token = generateRefreshToken({
      id: userInfo.id,
      email: userInfo.email,
      username: userInfo.username,
    });
    sendRefreshToken(res, refresh_token);
    sendAccessToken(res, access_token);
  });
};
