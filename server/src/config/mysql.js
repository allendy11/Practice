const mysql = require("mysql");
const { mysql_env } = require("./config");

const env = {
  host: mysql_env.host,
  user: mysql_env.user,
  password: mysql_env.password,
  database: mysql_env.database,
  port: mysql_env.port,
};

const Connect = () => {
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
const Query = (connection, query, params = null) => {
  if (params) {
    return new Promise((resolve, reject) => {
      connection.query(query, params, (error, result) => {
        if (error) {
          reject(error);
        } else {
          resolve(result);
        }
      });
    });
  } else {
    return new Promise((resolve, reject) => {
      connection.query(query, (error, result) => {
        if (error) {
          reject(error);
        } else {
          resolve(result);
        }
      });
    });
  }
};
module.exports = { Connect, Query };
