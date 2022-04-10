const { User } = require("../../models");

module.exports = (req, res) => {
  User.findByPk(req.params.id).then((userInfo) => {
    if (!userInfo) {
      res.status(404).json({ message: "user not found" });
    } else {
      res.status(200).json({
        data: {
          id: userInfo.id,
          name: userInfo.name,
          email: userInfo.email,
        },
        message: "get userInfo complete",
      });
    }
  });
};
