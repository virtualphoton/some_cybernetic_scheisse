import React, { useEffect, useState } from "react";
import { BACKEND_URL } from "../App";
import Axios from "axios";
import { useNavigate } from "react-router";
import { config } from "../utils";
import { handleLogout } from "./SignIn/Signin";

export default function LoggedIn() {
  const [auth, setAuth] = useState(null);
  const nav = useNavigate();

  useEffect(() => {
    if (localStorage.getItem('JWT') === null){
      return nav("/login")
    } else {
      Axios.get(`${BACKEND_URL}/home`, config()).then((res) => {
        console.log(res)
        setAuth(res.data)
      }).catch((err) => console.log(err));
      }
  }, [])

  
  return (
    <div style={{padding:"10px", border:"2px solid black", margin:"20px"}}>
      <img src={auth ? auth["picture"]:""} alt="Profile picture" />
      <h1>Hello {auth ? auth["name"]:""}, Welcome to Skionetizy</h1>
      <h2>Email: {auth ? auth["email"]:""}</h2>
      <button onClick={() => handleLogout(nav)}>Logout</button>
    </div>
  );
}
