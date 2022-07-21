module.exports = (req, res) => {
  const { id, password } = req.body;
  if (id === "test" && password === "1234") {
    res.cookie(
      "access-token",
      "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9mzvUGDNV4EXqk"
    );
    res.cookie(
      "refresh-token",
      "jU0ODMzMTIwLCJleHAiOjE2NTQ4MzM3MjAsImlzcyI6InRvY"
    );
    res.status(200).json({
      message: "로그인 성공",
    });
  }
};
