const express = require("express");
const router = express.Router();
const { signin, signup, signout } = require("../controllers");
/* GET users listing. */
router.post("/signin", signin);
router.post("/signup", signup);
router.signout("/signout", signout);

module.exports = router;
