import { ReactTerminal } from "react-terminal";
import { Dropdown } from 'semantic-ui-react';
import React, { useState, useRef, useEffect } from 'react';
import Axios from "axios";

import { BACKEND_URL } from "../../App";
import { config } from "../../utils";

const default_commands = {
  cd: (directory, dir2) => `changed path to ${directory}, ${dir2}`
};

function CommandSender(setResult, machine_id, command, args) {
  const query = new URLSearchParams(window.location.search);
  let group_id = query.get("group_id");
  
  Axios.post(
    `${BACKEND_URL}/machine_commands`, {
      "group_id": group_id, "machine_id": machine_id,
      "command": command, "args": args
    }, config()
  ).then(response => {setResult(JSON.stringify(response.data.msg, null, 2));}).catch(
    err => {setResult(JSON.stringify(err.data, null, 2))}
  );
}

function MachineSelector(machines) {
  const [selected, setSelected] = useState({name : "", id : -1});
  useEffect(
    () => {
      if (machines.length)
        setSelected(machines[0]);
    },
    [machines]
  );
  //onChange={(_, {value}) => setSelected(cameras.find(camera => camera.id === value))}
  let choice = machines.map(machine => {return {key: machine.id, value: machine.id, text: machine.name}});
  return [(
    <Dropdown selection
              value={selected.id}
              text={selected.name}
              onChange={(_, {value}) => {setSelected(machines.find(machine => machine.id === value))}}
              options={choice}
              />
  ), selected]
}


function Terminal(machines) {
  const [result, setResult] = useState("");
  const [terminals, setTerminals] = useState([]);
  const [machineSelector, machine] = MachineSelector(machines);
  
  // build dict: machine.id -> terminal
  useEffect(() => {
    setTerminals(machines.reduce((obj, machine) => 
      (obj[machine.id] = 
        <ReactTerminal
          prompt={`${machine.id}$`}
          defaultHandler={(command, ...args) => CommandSender(setResult, machine.id, command, ...args)}
          commands={default_commands}
        />, obj), {})
    )
  }, [machines]);

  return (
    <div>
      {machineSelector}
      {terminals[machine.id]}
      <p>{result}</p>
    </div>
  )
}

export default Terminal;
