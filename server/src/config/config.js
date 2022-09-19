require("dotenv").config();

// SERVER
const server_host = process.env.SERVER_HOST || "localhost";
const server_port = process.env.SERVER_PORT || "4000";
const token_issuer = process.env.TOKEN_ISSUER || "root";
const token_secret = process.env.TOKEN_SECRET || "secret";
const token_expire_time = process.env.TOKEN_EXPIRE_TIME || "10m";
const hash_salt = process.env.HASH_SALT || "10";

const server_env = {
  host: server_host,
  port: server_port,
  token: {
    issuer: token_issuer,
    secret: token_secret,
    expireTime: token_expire_time,
  },
  hash: {
    salt: parseInt(hash_salt),
  },
};

// MYSQL
const mysql_host = process.env.MYSQL_HOST || "localhost";
const mysql_user = process.env.MYSQL_USER || "root";
const mysql_password = process.env.MYSQL_PASSWORD || "password";
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
