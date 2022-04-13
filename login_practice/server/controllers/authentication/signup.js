const { User } = require("../../models");

module.exports = (req, res) => {
  User.findOne({
    where: {
      email: req.body.email,
    },
  })
    .then((userInfo) => {
      if (userInfo) {
        return res.status(401).json({ message: "email exist" });
      }
    })
    .then(() => {
      User.create({
        username: req.body.username,
        email: req.body.email,
        password: req.body.password,
      });
      res.status(201).json({ message: "signup ok" });
    });
};
