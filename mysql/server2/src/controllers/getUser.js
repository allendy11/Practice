import models from "../models";

module.exports = (req, res) => {
  models.getUser((err, result) => {
    if (err) console.log(err);
    else {
      res.send(result);
    }
  });
};
