const express = require("express");
const router = express.Router();
const { userInfo } = require("../controllers");

router("/", userInfo);

module.exports = router;
