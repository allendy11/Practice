require("dotenv").config();
const https = require("https");
const http = require("http");
const cors = require("cors");
const express = require("express");
const app = express();
const cookieParser = require("cookie-parser");
app.use(express.json());
app.use(
  cors({
    origin: "http://localhost:3000",
    credentials: true,
    methods: ["GET", "POST", "OPTIONS"],
  })
);
app.use(cookieParser());

const port = process.env.port || 4000;
let server;
server = http.createServer(app);
server.listen(port, () => console.log(`listen on ${port}`));
