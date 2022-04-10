const { checkAccessToken } = require("../tokenFunctions");
module.exports = (req, res) => {
  const data = checkAccessToken(req);
  if (!data) {
    res.status(404).json({ message: "token is expired" });
  } else {
    res.clearCookie("refreshToken");
    res.status(200).json({ message: "signout complete" });
  }
};
