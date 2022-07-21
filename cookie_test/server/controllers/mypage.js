module.exports = (req, res) => {
  const cookies = req.cookies;
  if (
    cookies["access-token"] ===
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9mzvUGDNV4EXqk"
  ) {
    res.status(200).json({
      name: "test",
      email: "test@test.com",
      mobile: "010-1234-1234",
    });
  } else {
    res.status(401).json({
      message: "Unauthrized token",
    });
  }
};
