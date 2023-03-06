import { ReactTerminal } from "react-terminal";
import { Dropdown } from 'semantic-ui-react';
import React, { useState, useRef, useEffect } from 'react';
import Axios from "axios";

const LOCAL_STORAGE_TERMINAL_KEY = 'someApp.terminal'
const default_commands = {
  cd: (directory, dir2) => `changed path to ${directory}, ${dir2}`
};

function CommandSender(terminal, command, args) {
  return command;
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
  const [terminals, setTerminals] = useState([]);
  const [machineSelector, machine] = MachineSelector(machines);
  
  // build dict: machine.id -> terminal
  useEffect(() => {
    setTerminals(machines.reduce((obj, machine) => 
      (obj[machine.id] = 
        <ReactTerminal
          prompt={`${machine.id}$`}
          defaultHandler={(...args) => CommandSender(terminals[machine.id], ...args)}
          commands={default_commands}
        />, obj), {})
    )
  }, [machines]);

  return (
    <div>
      {machineSelector}
      {terminals[machine.id]}
    </div>
  )
}

export default Terminal;
