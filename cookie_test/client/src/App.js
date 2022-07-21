import { useState } from "react";
import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Nav from "./components/Nav/Nav";
import Landing from "./pages/Landing";
import Login from "./pages/Login";
import Mypage from "./pages/Mypage";
function App() {
  const [isLogin, setIsLogin] = useState(false);
  return (
    <div id="App">
      <Router>
        <Nav isLogin={isLogin} setIsLogin={setIsLogin} />
        <Routes>
          <Route
            path="/"
            element={<Landing isLogin={isLogin} setIsLogin={setIsLogin} />}
          />
          <Route
            path="/login"
            element={<Login isLogin={isLogin} setIsLogin={setIsLogin} />}
          />
          <Route
            path="/mypage"
            element={<Mypage isLogin={isLogin} setIsLogin={setIsLogin} />}
          />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
