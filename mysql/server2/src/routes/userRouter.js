import express from "express";
import { getUser, postUser, testPost } from "../controllers";

const router = express.Router();

router.get("/", getUser);
router.post("/", postUser);
router.post("/test", testPost);

module.exports = router;
