import { ReactTerminal } from "react-terminal";
import React, { useState, useRef, useEffect } from 'react';
import axios from "axios";

const LOCAL_STORAGE_TERMINAL_KEY = 'someApp.terminal'
const default_commands = {
  cd: (directory, dir2) => `changed path to ${directory}, ${dir2}`
};

function CommandSender(terminal, command, args) {
  return command;
}

function MachineSelector(machines) {
  const [selected, setSelected] = useState({id:-1, name:""});
  
  useEffect(() => {
    const storedTodos = JSON.parse(localStorage.getItem(LOCAL_STORAGE_TERMINAL_KEY))
    if (storedTodos) setActiveTerm(storedTodos)
  }, []);
  useEffect(() => {
    localStorage.setItem(LOCAL_STORAGE_TERMINAL_KEY, JSON.stringify(activeTerm))
  }, [activeTerm]);

  
  return [(
    <Dropdown text={selected.name}
              value={selected.id}
              onChange={(_, {value}) => setSelected(machines.find(machine => machine.id === value))}>
                
      <Dropdown.Menu>
        {machines.map(machine =>
          <Dropdown.Item text={machine.name} key={machine.id}/>
        )}
      </Dropdown.Menu>
    </Dropdown>
  ), selected];
}


function Terminal(machines) {
  let machines = prop.machines;
  
  const [terminals, setTerminals] = useState([]);
  const [machineSelector, machine] = MachineSelector(cameras);
  
  // build dict: machine.id -> terminal
  useEffect(() => {
    setTerminals(machines.reduce((obj, machine) => 
      (obj[machine.id] = 
        <ReactTerminal
          prompt={`${machine.id}$`}
          defaultHandler={(...args) => CommandSender(terminals[activeTerm], ...args)}
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
