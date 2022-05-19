const http = require("http");
const express = require("express");
const cors = require("cors");

const app = express();
const router = express.Router();
app.use(
  cors({
    origin: "http://localhost:3000",
    methods: ["OPTIONS", "GET", "POST"],
    credentials: true,
  })
);
// app.use("/user", userRouter);
let server = http.createServer(app);
const port = 3000;
server.listen(port, () => console.log(`listen on ${port}`));
