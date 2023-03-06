import React, {useEffect, useState, useRef} from "react";
import { Table } from 'semantic-ui-react'
import { callDbApi, callApiInto } from "../utils"

function Machine(prop) {
  return (
    <Table.Row>
        <Table.Cell>{prop.name}</Table.Cell>
        <Table.Cell>{prop.jspath}</Table.Cell>
    </Table.Row>
  )
}

function Camera(prop) {
  return (
    <Table.Row>
        <Table.Cell>{prop.name}</Table.Cell>
        <Table.Cell>{prop.connection}</Table.Cell>
        <Table.Cell>{prop.address}</Table.Cell>
    </Table.Row>
  )
}

export default function Resources() {
  const [machines, setMachines] = useState([]);
  const [cameras, setCameras] = useState([]);
  useEffect(callApiInto("list_resources", setMachines, {resource_type: "machine"}), []);
  useEffect(callApiInto("list_resources", setCameras, {resource_type: "camera"}), []);
  console.log(machines);
  return (
    <>
    <h3>Machines</h3>
    <Table celled>
      <Table.Header>
        <Table.Row>
          <Table.HeaderCell>Name</Table.HeaderCell>
          <Table.HeaderCell>JS path</Table.HeaderCell>
        </Table.Row>
      </Table.Header>
      
      <Table.Body>
        {machines.map(machine =>
          <Machine
            key={machine.id}
            name={machine.name}
            jspath={machine.js_path}
          />
        )}
      </Table.Body>
    </Table>
    
    <h3>Cameras</h3>
    <Table celled>
      <Table.Header>
        <Table.Row>
          <Table.HeaderCell>Name</Table.HeaderCell>
          <Table.HeaderCell>Connection type</Table.HeaderCell>
          <Table.HeaderCell>Address</Table.HeaderCell>
        </Table.Row>
      </Table.Header>
      
      <Table.Body>
        {cameras.map(camera =>
          <Camera
            key={camera.id}
            name={camera.name}
            connection={camera.connection}
            address={camera.address}
          />
        )}
      </Table.Body>
    </Table>
    </>
  );
};