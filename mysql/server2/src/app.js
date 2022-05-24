import express, { urlencoded } from "express";
import cookieParser from "cookie-parser";
import logger from "morgan";
import cors from "cors";
import dotenv from "dotenv";
import userRouter from "./routes/userRouter";

dotenv.config();

const app = express();
const port = process.env.PORT || 4000;

app.use(express.json());
app.use(cookieParser());
app.use(urlencoded({ extended: false }));
app.use(logger("dev"));

app.use("/user", userRouter);

const server = app.listen(port, () => console.log(`listen on ${port}`));

module.exports = server;
