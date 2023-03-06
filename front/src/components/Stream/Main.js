import React, { useState, useRef, useEffect } from 'react';
import {TerminalContextProvider} from "react-terminal";
import Terminal from "./Terminal";
import styled from "styled-components";

import { callApiInto } from '../../utils';
import Cam from './Cameras';

const Flexed = styled.div`
  display: flex;
  justify-content: flex-start;
`

export default function Stream() {
  const [group, setGroup] = useState({id: null, name: "", description: "",
                                      cameras: [], machines: []});
  //{id: null, name: "", res_x: 0, res_y: 0}
  const [machines, setMachines] = useState([]);
  //{id: null, name: "", aruco_id: 0, commands: []}
  const [cameras, setCameras] = useState([]);
  
  const query = new URLSearchParams(window.location.search);
  let group_id = query.get("group_id");
  useEffect(callApiInto("get_group", setGroup, {group_id: Number(group_id)}), []);
  
  useEffect(
    callApiInto(
      "get_resources",
      setMachines, 
      {resource_type: "machine", res_ids: group.machines}
    ), [group]
  );
  useEffect(
    callApiInto(
      "get_resources",
      setCameras, 
      {resource_type: "camera", res_ids: group.cameras}
    ), [group]
  );
  
  return (
    <TerminalContextProvider>
      <Flexed>
        {Cam(cameras)}
      </Flexed>
      
      {Terminal(machines)}
    </TerminalContextProvider>
  )
}
