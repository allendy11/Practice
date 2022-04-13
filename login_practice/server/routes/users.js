const express = require("express");
const router = express.Router();
const { signin, signup, signout, userInfo } = require("../controllers");
/* GET users listing. */
router.get("/", userInfo);
router.post("/signin", signin);
router.post("/signup", signup);
router.post("/signout", signout);
module.exports = router;
