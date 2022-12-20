import React, {useEffect, useState, useRef} from "react";
import MachineButton from "./Machine";
import axios from 'axios';

function useInterval(callback, delay) {
  const savedCallback = useRef();

  // Remember the latest callback.
  useEffect(() => {
    savedCallback.current = callback;
  }, [callback]);

  // Set up the interval.
  useEffect(() => {
    function tick() {
      savedCallback.current();
    }
    if (delay !== null) {
      let id = setInterval(tick, delay);
      return () => clearInterval(id);
    }
  }, [delay]);
}


function Machines() {
  const [machines, set_data] = useState([])
  useInterval(() => {
    axios.get("/get_machines").then((response) => {
      set_data(response.data);
    });
  }, 1000);

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
