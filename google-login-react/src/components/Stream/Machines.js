import { Button } from 'semantic-ui-react'
import React, {useEffect, useState, useRef} from "react";
import Axios from 'axios';
import styled from "styled-components";

import { BACKEND_URL } from '../../App';
import { config } from '../../utils';

function toggleState(id, action) {
  return () => 
  Axios.post(`${BACKEND_URL}/toggle_state`, {button_id: id, action: action}, config())
         .then(res => console.log(res)) // TODO delete
         .catch(err => console.log(err))
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
        <Button negative
                onClick={toggleState(prop.aruco_id, "disable")}
                content="Disconnect"
        />
        <p>{prop.name}</p>
      </Device>
    );
  } else {
    return (
      <Device>
        <Button positive
                onClick={toggleState(prop.aruco_id, "enable")}
                content="Connect"
        />
        <p>{prop.name}</p>
      </Device>
    );
  }
}


function Machines(prop) {
  let machines = prop.machines;

  return (
    <div>
      {machines.map(machine =>
        <MachineButton
          key={machine.aruco_id}
          aruco_id={machine.aruco_id}
          name={machine.name}
          connected={machine.connected}
        />
      )}
    </div>
  );
}

export default Machines;
