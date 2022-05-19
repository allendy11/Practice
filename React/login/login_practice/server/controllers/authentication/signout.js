const { User } = require("../../models");
const { checkAccessToken, clearRefreshToken } = require("./tokenFunctions");
module.exports = (req, res) => {
  const auth = checkAccessToken(req);
  if (!req) {
    res.status(404).json({ message: "not authorized" });
  }
  clearRefreshToken(res);
};
