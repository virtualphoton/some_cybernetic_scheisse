import React, {useEffect, useState, useRef} from "react";
import axios from 'axios';
import styled from "styled-components";

const ButtonOff = styled.button`
  background-color: green;
  color: white;
  font-size: 20px;
  padding: 10px 60px;
  border-radius: 5px;
  margin: 10px 0px;
  cursor: pointer;
`;

const ButtonOn = styled.button`
  background-color: red;
  color: white;
  font-size: 20px;
  padding: 10px 60px;
  border-radius: 5px;
  margin: 10px 0px;
  cursor: pointer;
`;

function toggleState(event) {
  console.log(event)
  let id = event.target.id;
  console.log(id)
  if (id.startsWith('b_')) {
    axios
      .post("/toggle_state", {button_id: id})
      .then(res => console.log(res))
      .catch(err => console.log(err))
  }
}

const Device = styled.div`
  display: flex;
  justify-content: flex-start;
  align-items: center;
`

function MachineButton(prop) {
  if (prop.connected) {
    return (
      <Device>
        <ButtonOn id={"b_off_" + prop.aruco_id} onClick={toggleState}>Disconnect</ButtonOn>
        <p>{prop.name}</p>
      </Device>
    );
  } else {
    return (
      <Device>
        <ButtonOff id={"b_on_" + prop.aruco_id} onClick={toggleState}>Connect</ButtonOff>
        <p>{prop.name}</p>
      </Device>
    );
  }
}

export default MachineButton;
