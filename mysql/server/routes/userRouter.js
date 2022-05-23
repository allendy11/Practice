const express = require("express");
const router = express.Router();
const { user } = require("../controllers");

router.get("/", user);

module.exports = router;
