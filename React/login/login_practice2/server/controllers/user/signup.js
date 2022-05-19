const { User } = require("../../models");
module.exports = (req, res) => {
  User.findOrCreate({
    where: {
      email: req.body.email,
    },
    defaults: {
      name: req.body.name,
      password: req.body.password,
    },
  }).then(([user, created]) => {
    if (!created) {
      res.status(401).json({
        message: "email exist already",
      });
    } else {
      res.status(200).json({
        message: "signup complete",
      });
    }
  });
};
