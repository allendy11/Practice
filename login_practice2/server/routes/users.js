const express = require("express");
const router = express.Router();
const controllers = require("../controllers");
/* GET users listing. */
router.post("/signin", controllers.signin);
router.post("/signout", controllers.signout);
router.post("/signup", controllers.signup);
router.get("/:id", controllers.profile);

module.exports = router;
