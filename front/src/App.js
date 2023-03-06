import Axios from "axios";
import React, {useEffect } from "react";
import { Routes, Route, useLocation} from "react-router-dom";
import { useNavigate } from "react-router";

import Groups from "./components/Groups/Groups";
import GroupModification from "./components/Groups/GroupModification";
import Signin from "./components/SignIn/Signin";
import TopMenu from "./TopMenu";
import Users from "./components/Users";
import Console from "./components/Console";
import Stream from "./components/Stream/Main";
import Resources from "./components/Resources";
import { isAdmin, isLoggedIn } from "./utils";

export const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

const allowedForUser = ["login", "groups"]

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
      const role = query.get('role')
      if (token) {
        localStorage.setItem('JWT', token);
        localStorage.setItem('role', role);
        return nav('/groups')
      } else if (location.pathname != "/login") {
        return nav('/login');
      }
    }
    if (isLoggedIn() && !isAdmin() && !allowedForUser.includes(location.pathname)) {
      return nav('/groups');
    }
  }, [])
  
  let topMenu;
  if (isLoggedIn()) {
    topMenu = <TopMenu path={location.pathname}/>
  } else {
    topMenu = <></>
  }
  
  return (
    <>
      {topMenu}
      
      <Routes>
        <Route
          exact
          path="/login"
          element={<Signin login={handleClick}></Signin>}
        />
        <Route exact path="/groups" element={<Groups/>} />
        
        <Route exact path="/users" element={<Users/>} />
        <Route exact path="/modifygroup" element={<GroupModification/>} />
        <Route exact path="/console" element={<Console/>} />
        <Route exact path="/stream" element={<Stream/>} />
        <Route exact path="/resources" element={<Resources/>} />
        <Route exact path="/"/>
      </Routes>
    </>
  );
}

export default App;
