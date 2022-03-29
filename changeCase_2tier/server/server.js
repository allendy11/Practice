const http = require("http");
const requestHandler = require("./requestHandler");
const port = 4000;
let server = http.createServer(requestHandler);
server.listen(port, () => {
  console.log(`listen on ${port}`);
});
