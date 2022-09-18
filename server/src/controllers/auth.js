const bcryptjs = require("bcryptjs");
const { Connect } = require("../config/mysql");
const { server_env } = require("../config/config");
const logger = require("../config/logger");

const NAMESPACE = "Auth";

const register = async (ctx, next) => {
  const { name, email, password } = ctx.request.body;
  console.log(name, email, password);

  // hashing password;
  bcryptjs.hash(password, server_env.hash.salt, (error, hash) => {
    logger.info(NAMESPACE, "hashing password");
    if (error) {
      logger.error(NAMESPACE, error.message);
    } else {
      // console.log(hash);
      const query = "INSERT INTO users (name, email, password) values (?,?,?)";
      const params = [name, email, hash];
      Connect().then((connection) => {
        Query(connection, query, params).then((result) => {
          console.log(result);
        });
      });
    }
  });

  // else {
  //   connect().then((connection) => {
  //     connection.query(query, params, (error, result) => {
  //       if (error) {
  //         // ctx.throw(error.message);
  //       } else {
  //         // ctx.throw(result);
  //       }
  //     });
  //   });
  // }
};

const login = (ctx, next) => {
  const { email, password } = ctx.request.body;
  console.log(email, password);
};

const logout = (ctx, next) => {};
const validate = (ctx, next) => {};

const deleteAccount = (ctx, next) => {};

module.exports = { register, login };
