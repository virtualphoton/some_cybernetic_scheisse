import React, { Component, useState } from "react";
import { Button, Menu, Dropdown } from "semantic-ui-react";
import { Link, useLocation, useNavigate} from "react-router-dom";

import {handleLogout} from "./components/SignIn/Signin"

export default function TopMenu(prop) {
  const location = useLocation();
  const locChecker = (path => location.pathname === path);
  
  let nav = useNavigate();
  
  return (
    <Menu>
      <Menu.Item active={locChecker("/stream")}
                 as={Link} to="/stream"
                 content="Stream"/>
      
      <Menu.Item active={locChecker("/groups")}
                 as={Link} to="/groups"
                 content="Groups"/>
      
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
                 
      <Menu.Item position="right">
        <Button onClick={() => handleLogout(nav)}>Log out</Button>
      </Menu.Item>
    </Menu>
  )
}
