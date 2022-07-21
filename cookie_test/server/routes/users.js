const express = require("express");
const router = express.Router();
const { login, mypage } = require("../controllers");
/* GET users listing. */
router.get("/", function (req, res, next) {
  res.send("respond with a resource");
});
router.post("/login", login);
router.get("/mypage", mypage);
module.exports = router;
