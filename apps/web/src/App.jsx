import { Layout } from "@consta/uikit/Layout";
import Home from "./page/Home";
import "./App.css";
import Header from "./components/header/Header";
import { Route, Routes } from "react-router-dom";
import SingleVideo from "./page/SingleVideo";
import AddVideo from "./page/AddVideo";
import Footer from "./components/Footer";

function App() {
  return (
    <>
      <Layout direction="column" style={{ minHeight: "100vh" }}>
        <Header />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/video/:id" element={<SingleVideo />} />
          <Route path="/add" element={<AddVideo />} />
        </Routes>
        <Footer />
      </Layout>
    </>
  );
}

export default App;
