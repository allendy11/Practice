module.exports = {
  env: {
    browser: true,
    commonjs: true,
    es2021: true,
  },
  extends: [
    // "eslint:recommended",
    // "plugin:react/recommended"
    "standard",
  ],
  overrides: [],
  parserOptions: {
    ecmaVersion: "latest",
  },
  plugins: ["react"],
  rules: {
    indent: ["error", 4],
    semi: ["error", "always"],
    "no-trailing-spaces": 0,
    "keyword-spacing": 0,
    "no-unused-vars": 1,
    "no-multiple-empty-lines": 0,
    "space-before-function-paren": 0,
    "eol-last": 0,
  },
};
