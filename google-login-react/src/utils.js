import Axios from "axios";
import { BACKEND_URL } from "./App";

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
  return () => {callDbApi(method, data).then(response => setState(response.data))};
}