import React, {useEffect, useState, useRef} from "react";
import { Table, Tab, Button } from "semantic-ui-react";
import { callApiInto } from "../../utils";
import { Link, useLocation, useNavigate} from "react-router-dom";

function Group(prop) {
  return (
    <Table.Row>
        <Table.Cell>{prop.name}</Table.Cell>
    </Table.Row>
  )
}

function GroupsICreated() {
  const [groups, setGroups] = useState([]);
  
  useEffect(callApiInto("list_groups", setGroups), []);
  
  
  let table = <></>;
  if (groups.length) {
    table = (
      <Table selectable>
        <Table.Header>
          <Table.Row>
            <Table.HeaderCell>Name</Table.HeaderCell>
          </Table.Row>
        </Table.Header>
        
        <Table.Body>
          {groups.map(user =>
            <Group
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
  
  return (
    <>
    { table }
    <Button positive icon="plus"
            href="/modifygroup"/>
    </>
  )
}

function GroupsIAmIn() {
  const [groups, setGroups] = useState([])
  
  useEffect(callApiInto("list_groups_i_am_in", setGroups), []);
  
  return (
    <Table>
      <Table.Header>
        <Table.Row>
          <Table.HeaderCell>Name</Table.HeaderCell>
        </Table.Row>
      </Table.Header>
      
      <Table.Body>
        {groups.map(user =>
          <Group
            key={user.email}
            username={user.username}
            email={user.email}
            role={user.role}
          />
        )}
      </Table.Body>
    </Table>
  )
}

function Groups() {
  let groupsIAmIn = GroupsIAmIn();
  let groupsICreated = GroupsICreated();
  const panes = [
    { menuItem: 'Groups I am in', render: () => <Tab.Pane>{groupsIAmIn}</Tab.Pane>},
    { menuItem: 'Groups I created', render: () => <Tab.Pane>{groupsICreated}</Tab.Pane> },
  ]
  return <Tab panes={panes} />
}

export default Groups;