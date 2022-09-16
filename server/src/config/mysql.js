const mysql = require("mysql");
const { mysql_env } = require("./config");

const env = {
  host: mysql_env.host,
  user: mysql_env.user,
  password: mysql_env.password,
  database: mysql_env.database,
  port: mysql_env.port,
};

const connect = () => {
  return new Promise((resolve, reject) => {
    const connection = mysql.createConnection(env);

    connection.connect((error) => {
      if (error) {
        reject(error);
      } else {
        resolve(connection);
      }
    });
  });
};

module.exports = { connect };
