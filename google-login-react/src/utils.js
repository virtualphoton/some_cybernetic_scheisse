import Axios from "axios";
import { BACKEND_URL } from "./App";
import { handleLogout } from "./components/SignIn/Signin";

export function config() {
  return {"headers" : {
    "Authorization": `Bearer ${localStorage.getItem('JWT')}`
  }}
}

export function callDbApi(func, data={}) {
  return Axios.post(
    `${BACKEND_URL}/db_api/${func}`, 
    data, config()
  )
}

export function callApiInto(method, setState, data={}) {
  return () => callDbApi(method, data).then(response => setState(response.data)).catch(
    err => {
      if (err.response.status == 401) {
        handleLogout();
      }
    }
  );
}

export function isAdmin() {
  return isLoggedIn && localStorage.getItem('role') == "admin";
}

export function isLoggedIn() {
  return localStorage.getItem('JWT') !== null;
}