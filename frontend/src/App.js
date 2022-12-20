import React, { useState } from "react";
import { ReactTerminal } from "react-terminal";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Main from './pages/Main'
import Login from './pages/Login'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Main/>}>
          <Route path="login" element={<Login />} />
          <Route path="*" element={<Main/>} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
