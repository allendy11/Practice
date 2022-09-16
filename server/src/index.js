const Koa = require("koa");
const Router = require("koa-router");
const logger = require("koa-logger");

const { server_env } = require("./config/config");

const userRouter = require("./routes/userRouter");
const testRouter = require("./routes/testRouter");
const app = new Koa();
const router = new Router();

// Middleware: Logger
app.use(logger());

// init
app.use((ctx, next) => {
  ctx.body = "Hello, world!";
  console.log("Hello, world!");
  next();
});

// Routes : home
router.get("/", (ctx, next) => {
  ctx.body = "home";
});

// Routes : user
router.use("/user", userRouter.routes());

// Routes : test
router.use("/test", testRouter.routes());

// SET router
app.use(router.routes()).use(router.allowedMethods());

// CREATE server
app.listen(server_env.port, () => {
  console.log(`Listen on ${server_env.port}`);
});
