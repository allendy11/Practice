import db from "../db";

module.exports = {
  getUser: (cb) => {
    const queryString = `select * from users`;
    db.query(queryString, (err, result) => {
      cb(err, result);
    });
  },
  postUser: (name, email, password, cb) => {
    const queryString = `insert into users (name, email, password) values (?,?,?)`;
    const params = [name, email, password];
    db.query(queryString, params, (err, result) => {
      cb(err, result);
    });
  },
  testPost: (name, cb) => {
    const queryString = `insert into users (name) values ?`;
    const params = name;
    db.query(queryString, [[[params]]], (err, result) => {
      cb(err, result);
    });
  },
};
