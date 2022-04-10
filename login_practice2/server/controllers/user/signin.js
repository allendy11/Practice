const { User } = require("../../models");
const {
  generateAccessToken,
  generateRefreshToken,
} = require("../tokenFunctions");

module.exports = (req, res) => {
  User.findOne({
    where: {
      email: req.body.email,
      password: req.body.password,
    },
  }).then((userInfo) => {
    if (!userInfo) {
      res.status(404).json({ message: "user not found" });
    } else {
      const data = {
        id: userInfo.id,
        name: userInfo.name,
        email: userInfo.email,
      };
      const accessToken = generateAccessToken(data);
      const refreshToken = generateRefreshToken(data);

      res.cookie("refreshToken", refreshToken); // refresh token 쿠키생성
      res.status(200).json({
        // access token 응답
        data: {
          accessToken,
        },
        message: "signin complete",
      });
    }
  });
};
