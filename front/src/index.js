import React from 'react';
import {BrowserRouter } from "react-router-dom";
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import { useNavigate } from 'react-router-dom';

import History from './History';

const NavigateSetter = () => {
  History.navigate = useNavigate();

  return null;
};

const styleLink = document.createElement("link");
styleLink.rel = "stylesheet";
styleLink.href = "https://cdn.jsdelivr.net/npm/semantic-ui/dist/semantic.min.css";
document.head.appendChild(styleLink);

ReactDOM.render(
    <BrowserRouter>
      <NavigateSetter />
      <App />
    </BrowserRouter>,
  document.getElementById("root")
);

