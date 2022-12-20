import { ReactTerminal } from "react-terminal";
import React, { useState, useRef, useEffect } from 'react';
import axios from "axios";

function CommandSender(terminal, command, args) {
  console.log(terminal.commands);
  if (!terminal.commands.includes(command)) {
    console.log("bad command!");
  } else {
    console.log("good command!");
  }
  console.log(args);
}

function ListActiveDevices() {
  return axios.get("/get_machines").then((response) => {
    let output = "";
      let machines = response.data;
      console.log(machines);
      console.log(machines
        .filter(machine => machine.connected));
      machines
        .filter(machine => machine.connected)
        .map(machine => output += `${machine.aruco_id} - ${machine.name}`);
      console.log(output);
      return output;
  });
}

function Activate(new_id, setTerminal) {
  return axios.post("/get_device_specs", {"aruco_id": new_id})
    .then((response) => {
      let data = response.data;
      console.log(data);
      setTerminal({
        "device_id": new_id,
        "device_prompt": `(${data['name']}) $`,
        "commands": data['commands']
      })
  });
}

function Deactivate(setTerminal) {
  setTerminal({
    "device_id": null,
    "device_prompt": "home $",
    "commands": [],
  });
}

const LOCAL_STORAGE_TERMINAL_KEY = 'someApp.terminal'

function Terminal() {
  const [terminal, setTerminal] = useState({
    "device_id": null,
    "device_prompt": "home $",
    "commands": [],
  })

  const default_commands = {
  "activate": (device) => Activate(device, setTerminal),
  "deactivate": () => Deactivate(setTerminal),
  "list": ListActiveDevices,
  cd: (directory, dir2) => `changed path to ${directory}, ${dir2}`
};

  useEffect(() => {
    const storedTodos = JSON.parse(localStorage.getItem(LOCAL_STORAGE_TERMINAL_KEY))
    if (storedTodos) setTerminal(storedTodos)
  }, [])

  useEffect(() => {
    localStorage.setItem(LOCAL_STORAGE_TERMINAL_KEY, JSON.stringify(terminal))
  }, [terminal])

  return (
    <ReactTerminal
      prompt={terminal.device_prompt}
      defaultHandler={(...args) => CommandSender(terminal, ...args)}
      commands={default_commands}
    />
  );
}

export default Terminal;
