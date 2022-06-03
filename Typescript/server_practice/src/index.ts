import express, { Request, Response, NextFunction } from "express";
import dotenv from "dotenv";
import cors from "cors";
import cookieParser from "cookie-parser";
dotenv.config();

const port: number = Number(process.env.PORT) || 4000;
const app = express();

app.use(express.json());

// 1. routes
app.get("/user", (req: Request, res: Response, next: NextFunction) => {
  res.sendStatus(200);
});
app.post("/user", (req: Request, res: Response, next: NextFunction) => {
  res.send(req.body);
});

// 2. chaining : 분기별로 작동된다. (모두 작동되는것이 아님)
app
  .route("/api")
  .get((req: Request, res: Response, next: NextFunction) => {
    res.send("get");
  })
  .post((req: Request, res: Response, next: NextFunction) => {
    res.send("post");
  })
  .put((req: Request, res: Response, next: NextFunction) => {
    res.send("put");
  });

// 3. path : * 부분의 어느 문자가 들어가도 응답할수있다. ex) localhost:4000/abdsfadsacd
app.get("/ab*cd", (req: Request, res: Response, next: NextFunction) => {
  res.send("ok");
});

// 4. params
app.get(
  "/user/:id/:name",
  (req: Request, res: Response, next: NextFunction) => {
    res.send({
      id: req.params.id,
      age: req.params.name,
    });
  }
);

// 5. route handler
function handleGetOne(req: Request, res: Response, next: NextFunction) {
  // res.send("one");
  next();
}
function handleGetTwo(req: Request, res: Response, next: NextFunction) {
  res.send("two");
}
app.get("/one", handleGetOne);
app.get("/onetwo", [handleGetOne, handleGetTwo]); // 배열을 통해 추가 가능

// 6. middleware
function middleware(req: Request, res: Response, next: NextFunction) {
  // @ts-ignore
  req.name = "Tom";
  next();
}
app.get(
  "/middleware",
  middleware, // 배열 형태로 추가 가능
  (req: Request, res: Response, next: NextFunction) => {
    // @ts-ignore
    res.send(req.name); //Tom
  }
);

// 6.1
const middleware2 =
  ({ name }: { name: string }) =>
  (req: Request, res: Response, next: NextFunction) => {
    // @ts-ignore
    req.name = name;
    next();
  };
app.use(middleware2({ name: "James" })); // 위치 주의
app.get("/middleware2", (req: Request, res: Response, next: NextFunction) => {
  //@ts-ignore
  res.send(req.name); //James
});

// 7. generic
const middleware3 =
  ({ name }: { name: string }) =>
  (req: Request, res: Response, next: NextFunction) => {
    res.locals.name = name;
    next();
  };
app.use(middleware3({ name: "James" })); // 위치 주의
app.get(
  "/middleware3/:id/:name",
  (
    req: Request<{ id: number; type: string }, {}, { name: string }, {}, {}>,
    res: Response,
    next: NextFunction
  ) => {
    req.params.id;
    req.body.name;
    res.send(res.locals.name);
  }
);

// 8. error handle
function errorHandler() {
  throw new Error("baaaaaad!!");
}
// 에러가 발생하면 그순간 멈추게 되고 응답이 되지않는다.
app.get("/error", (req: Request, res: Response, next: NextFunction) => {
  errorHandler(); // 멈춤
  res.status(400).send("something bad"); // 작동안함
});
// 8.1 위의 문제를 해결하기 위해 try/catch 사용
async function errorHandler2() {
  throw new Error("baaaaaad!!");
}
// 결과적으로 400 코드와 함께 something bad 뜨게 된다.
app.get("/error2", async (req: Request, res: Response, next: NextFunction) => {
  try {
    await errorHandler2(); // 에러 발생
    res.send(200).send("okk"); // 작동안함
  } catch (err) {
    res.status(400).send("something bad"); // 작동
  }
});

app.listen(port, () => {
  console.log(`listen on ${port}`);
});
