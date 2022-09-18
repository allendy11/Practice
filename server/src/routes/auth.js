const Router = require("koa-router");
const auth = require("../controllers/auth");
const router = new Router();

router.post("/register", auth.register);
router.post("/login", auth.login);

module.exports = router;
