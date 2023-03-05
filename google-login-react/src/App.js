import Axios from "axios";
import React, {useEffect } from "react";
import { Routes, Route, useLocation} from "react-router-dom";
import { useNavigate } from "react-router";

import Groups from "./components/Groups/Groups";
import GroupModification from "./components/Groups/GroupModification";
import Loggedin from "./components/Loggedin";
import Signin from "./components/SignIn/Signin";
import TopMenu from "./TopMenu";
import Users from "./components/Users";

export const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

function App() {
  const location = useLocation();
  
  const nav = useNavigate()
  const handleClick = (e) => {
    e.preventDefault();
    Axios.get(`${BACKEND_URL}/auth/google`, {
      headers: {
        "Access-Control-Allow-Origin": "* ",
        "Access-Control-Allow-Headers": "Content-Type",
      },
    }).then((res) => {
        // redirection to auth_url
        window.location.assign(res.data.auth_url);
    }).catch((err) => console.log(err));
    console.log(BACKEND_URL);
  };

  useEffect(() => {
    if (localStorage.getItem('JWT') == null){
      // get `jwt` param from url address after redirection
      const query = new URLSearchParams(window.location.search);
      const token = query.get('jwt')
      if (token) {
        localStorage.setItem('JWT', token);
        return nav('/home')
      } else if (location.pathname != "/login") {
        return nav('/login');
      }
    }
  })

  return (
    <>
      <TopMenu path={location.pathname}/>
      
      <Routes>
        <Route
          exact
          path="/login"
          element={<Signin login={handleClick}></Signin>}
        />
        <Route exact path="/home" element={<Loggedin></Loggedin>} />
        <Route exact path="/users" element={<Users/>} />
        <Route exact path="/groups" element={<Groups/>} />
        <Route exact path="/modifygroup" element={<GroupModification/>} />
        <Route exact path="/"/>
      </Routes>
    </>
  );
}

export default App;
