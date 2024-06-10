import { Layout } from "@consta/uikit/Layout";
import Home from "./page/Home";
import "./App.css";
import Header from "./components/header/Header";
import { Route, Routes } from "react-router-dom";
import SingleVideo from "./page/SingleVideo";

function App() {
  return (
    <>
      <Layout direction="column">
        <Header />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/video/:id" element={<SingleVideo />} />
        </Routes>
      </Layout>
    </>
  );
}

export default App;
