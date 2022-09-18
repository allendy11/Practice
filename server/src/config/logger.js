const info = (namespace, message) => {
  console.info(`[INFO] [${namespace}] ${message}`);
};
const error = (namespace, message, error = false) => {
  if (error) {
    console.error(`[ERROR] [${namespace}] ${message}`);
    console.error(error);
  } else {
    console.error(`[ERROR] [${namespace}] ${message}`);
  }
};
const end = (namespace, message) => {
  console.info(`[END] [${namespace}] ${message}`);
};
module.exports = {
  info,
  error,
  end,
};
