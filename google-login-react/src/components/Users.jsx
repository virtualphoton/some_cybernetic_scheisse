import React, {useEffect, useState, useRef} from "react";
import { Table } from 'semantic-ui-react'
import { callDbApi } from "../utils"

function User(prop) {
  return (
    <Table.Row>
        <Table.Cell>{prop.username}</Table.Cell>
        <Table.Cell>{prop.email}</Table.Cell>
        <Table.Cell>{prop.role}</Table.Cell>
    </Table.Row>
  )
}

function Users() {
  const [users, setData] = useState([])
  
  useEffect(() => {
    callDbApi("list_users").then(response => {
      setData(response.data);
    });
  }, []);
  
  return (
    <Table celled>
      <Table.Header>
        <Table.Row>
          <Table.HeaderCell>Name</Table.HeaderCell>
          <Table.HeaderCell>Email</Table.HeaderCell>
          <Table.HeaderCell>Role</Table.HeaderCell>
        </Table.Row>
      </Table.Header>
      
      <Table.Body>
        {users.map(user =>
          <User
            key={user.email}
            username={user.username}
            email={user.email}
            role={user.role}
          />
        )}
      </Table.Body>
    </Table>
  );
}

export default Users;