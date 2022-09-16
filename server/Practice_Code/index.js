const Koa = require("koa");
const Router = require("koa-router");
const logger = require("koa-logger");

const app = new Koa();

const router = new Router();

app.use(logger());

// basic use : 위치에 상관없이 라우터 보다 먼저 읽어들임
app.use((ctx, next) => {
  console.log(1);
  ctx.body = "Work at First";
  next(); // next 를 통해 다음 미들웨어나 라우터가 작동하게 된다.
});

// basic router : home
router.get("/", (ctx, next) => {
  ctx.body = "Home";
});

// next() return promise
router.get("/promise", (ctx, next) => {
  console.log(1);
  next().then(() => {
    console.log(2);
  });
});

// async/await
router.get("/async", async (ctx, next) => {
  console.log(3);
  await next();
  console.log(4);
});

// params
router.get("/about", (ctx, next) => {
  ctx.body = "about";
});
router.get("/about/:name", (ctx, next) => {
  const { name } = ctx.params;
  ctx.body = "about " + name;
});

// query
router.get("/post", (ctx, next) => {
  const { id } = ctx.request.query;
  if (id) {
    ctx.body = "post #" + id;
  } else {
    ctx.body = "There is no ID";
  }
});

// throw error
app.use((ctx, next) => {
  // const error = new Error("something wrong");
  // error.status = 400;
  // throw error;

  // 아래와 같이 쓸수있다.
  // ctx.throw(400, "something wrong");
  next();
});

// It doesn't work : express 와는 다르게 작동이 안되는듯
router.use((ctx, next) => {
  ctx.body = "Wrong path";
});

// allow router : 선언위치는 상관없어 보인다.
app.use(router.routes());
app.use(router.allowedMethods());

app.listen(4000, () => {
  console.log("Listen on 4000");
});
