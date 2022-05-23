const express = require("express");
const router = express.Router();
const { user } = require("../controllers");

router.get("/", (req, res) => {
  res.send("work");
});

module.exports = router;
