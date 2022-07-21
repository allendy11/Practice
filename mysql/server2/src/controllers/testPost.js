import models from "../models";

module.exports = (req, res) => {
  const { name, email, password } = req.body;
  models.testPost(name, (err, result) => {
    if (err) console.log(err);
    else {
      res.send(result);
    }
  });
};
