const { User } = require("../../models");
const { checkAccessToken } = require("../authentication/tokenFunctions");

module.exports = (req, res) => {
  const auth = checkAccessToken(req);
  if (!auth) {
    return res.status(404).json({ message: "unvalid accessToken or expired " });
  }
  res.status(200).send({ email: auth.email, username: auth.username });
};
