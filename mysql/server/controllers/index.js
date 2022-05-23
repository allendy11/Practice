const models = require("../models");
module.exports = {
  user: (req, res) => {
    models.get.user((err, result) => {
      if (err) throw err;
      else {
        res.send(result);
      }
    });
  },
};
