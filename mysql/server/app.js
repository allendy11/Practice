const express = require("express");
const cors = require("cors");
const cookieParser = require("cookie-parser");
const { urlencoded } = require("express");
const userRouter = require("./routes/userRouter");
const logger = require("morgan");

const app = express();
const port = 4000;

app.use(cookieParser());
app.use(express.json());
app.use(urlencoded({ extended: false }));
app.use(logger("dev"));
app.use(cors());

app.use("/user", userRouter);

const server = app.listen(port, () => console.log(`listen on ${port}`));

module.exports = server;
