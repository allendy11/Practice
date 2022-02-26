import logo from "./logo.svg";
import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Nav from "./components/Nav";
import Page1 from "./pages/Page1";
function App() {
  return (
    <div className="App">
      <Router>
        <Nav />
        <div className="pages_container">
          <Routes>
            <Route path="/page1" element={<Page1 />}></Route>
          </Routes>
        </div>
      </Router>
    </div>
  );
}

export default App;
