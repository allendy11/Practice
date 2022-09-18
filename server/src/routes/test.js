const Router = require("koa-router");
const test = require("../controllers/test");

const router = new Router();

router.get("/test", test);

module.exports = router;
