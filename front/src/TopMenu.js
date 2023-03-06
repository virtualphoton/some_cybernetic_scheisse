import React, { Component, useEffect, useState } from "react";
import { Button, Menu, Dropdown } from "semantic-ui-react";
import { Link, useLocation, useNavigate} from "react-router-dom";

import { handleLogout } from "./components/SignIn/Signin"
import { isAdmin } from "./utils";

export default function TopMenu(prop) {
  const location = useLocation();
  const locChecker = (path => location.pathname === path);
  
  let nav = useNavigate();
  let admin_panel;
  if (isAdmin()) {
    admin_panel = <>
      <Dropdown item text="Administrating"
                as={Menu.Item} active={locChecker("/users") || locChecker("/resources")}>
        <Dropdown.Menu>
          <Dropdown.Item onClick={() => nav("/resources")}>Resources</Dropdown.Item>
          <Dropdown.Item onClick={() => nav("/users")}>Users</Dropdown.Item >
        </Dropdown.Menu>
      </Dropdown>
      
      <Menu.Item active={locChecker("/console")}
                 as={Link} to="/console"
                 content="DB console"/>
    </>
  } else {
    admin_panel = <></>
  }
  
  return (
    <Menu>
      <Menu.Item active={locChecker("/groups")}
                 as={Link} to="/groups"
                 content="Groups"/>
      {admin_panel}
                 
      <Menu.Item position="right">
        <Button onClick={() => handleLogout()}>Log out</Button>
      </Menu.Item>
    </Menu>
  )
}
