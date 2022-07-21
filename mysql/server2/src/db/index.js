import mysql from "mysql";
import config from "../config";
import dotenv from "dotenv";
dotenv.config();

const con = mysql.createConnection(
  config[process.env.NODE_ENV || "development"]
);
con.connect((err) => {
  if (err) throw err;
});

module.exports = con;
