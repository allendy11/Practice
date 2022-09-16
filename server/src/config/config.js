require("dotenv").config();

// SERVER
const server_host = process.env.SERVER_HOST || "localhost";
const server_port = process.env.SErVER_PORT || "4000";

const server_env = {
  host: server_host,
  port: server_port,
};

// MYSQL
const mysql_host = process.env.MYSQL_HOST || "localhost";
const mysql_user = process.env.MYSQL_USER || "root";
const mysql_password = process.env.MYSQL_password || "password";
const mysql_database = process.env.MYSQL_DATABASE || "koa";
const mysql_port = process.env.MYSQL_PORT || "3306";

const mysql_env = {
  host: mysql_host,
  user: mysql_user,
  password: mysql_password,
  database: mysql_database,
  port: parseInt(mysql_port),
};

module.exports = {
  server_env,
  mysql_env,
};
