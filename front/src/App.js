import React from "react";
import { Helmet } from "react-helmet";
import { Routes, Route } from "react-router-dom";

import Landing from "./views/Landing.jsx";
import Login from "./views/Login.jsx";
import CheckIn from "./views/CheckIn.jsx";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

export default function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<Landing />}></Route>
        <Route path="/login" element={<Login />}></Route>
        <Route path="/checkin" element={<CheckIn />}></Route>
      </Routes>
      <ToastContainer />
    </>
  );
}
