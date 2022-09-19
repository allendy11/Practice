const Koa = require("koa");
const Router = require("koa-router");
const bodyParser = require("koa-bodyparser");

const { server_env } = require("./config/config");
const logger = require("./config/logger");

const authRouter = require("./routes/auth");
const testRouter = require("./routes/test");

const app = new Koa();
const router = new Router();

const NAMESPACE = "Server";

// Middleware
app.use(bodyParser());

// init
app.use((ctx, next) => {
  logger.info(NAMESPACE, `[method: ${ctx.method}] [path: ${ctx.path}]`);
  ctx.res.on("finish", () => {
    logger.end(
      NAMESPACE,
      `[status: ${ctx.res.statusCode}] [${ctx.res.statusMessage}]`
    );
  });
  next();
});

// Routes : home
router.get("/", (ctx, next) => {
  console.log("home");
  ctx.body = "Welcome home";
});

// Routes : user
router.use("/auth", authRouter.routes());

// Routes : test
router.use("/test", testRouter.routes());

// error 404: not found path
// app.use((ctx, next) => {
//   console.log();
//   const err = new Error("NOT FOUND");
//   err.status = 404;
//   err.expose = true;
//   throw err;
// });

// SET router
app.use(router.routes()).use(router.allowedMethods());

// CREATE server
app.listen(server_env.port, () => {
  console.log(`Listen on ${server_env.port}`);
});
