import React, { useEffect, useState } from 'react'
import { Button, Input, Form, Tab, TextArea, List, Dropdown } from 'semantic-ui-react'
import { useNavigate} from "react-router-dom";

import { callApiInto, callDbApi } from '../../utils';

function createPane(title, content) {
  return {
    menuItem: title,
    render: () => <Tab.Pane>{content}</Tab.Pane>
  };
}

function makeStrNonEmpry(str) {
  return str === ""? " " : str
}

function toIds(arr) {
  return arr.map(item => item.id);
}

export function renderList(items, repr, additionalContent = null) {
  if (additionalContent === null) {
    additionalContent = () => <></>
  }
  
  return (
    <List divided verticalAlign='middle'>
      {items.map(item =>
        <List.Item key={item.id}>
          <List.Content floated='right'>
            {additionalContent(item)}
          </List.Content>
          
          <List.Content content={repr(item)}/>
        </List.Item>
      )}
    </List>
  )
}

function AppendableList(retrieve_all, selected_ids_sent, repr) {
  const [all, setAll] = useState([]);
  const [selected, setSelected] = useState([]);
  const [unselectedList, setUnselected] = useState([]);
  
  useEffect(retrieve_all(setAll), []);
  useEffect(() => setSelected(all.filter(item => selected_ids_sent.includes(item.id))), [all, selected_ids_sent]);
  useEffect(() => {
    let used_ids = selected.map(item => item.id);
    let unselected = all.filter(item => !used_ids.includes(item.id))
    setUnselected(unselected.map(
      item => {return {key: item.id, value: item.id, text: repr(item)}}
    ));
  }, [selected]);
  
  function deleter(id) {
    return () => setSelected(selected.filter(item => item.id !== id));
  }
  
  return [(
    <>
    {renderList(selected, repr, (item) =>
      <Button negative
              icon="close"
              onClick={deleter(item.id)}
      />
    )}
    
    <Dropdown placeholder='Add new (Esc, to close selection)'
              search selection
              value={""}
              options={unselectedList}
              onChange={(_, {value}) => 
              setSelected([...selected, all.find(item => item.id === value)])}
    />
    </>
  ), selected];
}

function DescriptionTab(groupReceived) {
  const [name, setName] = useState("");
  const [descr, setDescr] = useState(" ");
  
  useEffect(() => {
    setName(groupReceived.name);
    setDescr(makeStrNonEmpry(groupReceived.description));
  }, [groupReceived])
  
  return [(
    <Form>
      <Form.Field name='name'
                  control={Input}
                  value={name}
                  label='Group name'
                  onChange={(e, { value }) => setName(value)}
      />
      
      <Form.Field name='description'
                  control={TextArea}
                  value={descr}
                  label='Group description'
                  onChange={(e, { value }) => setDescr(makeStrNonEmpry(value))}
      />
    </Form>
  ), name, descr]
}

export default function ModifyGroup() {
  const [group, setGroup] = useState({id: null, name: "", description: "",
                                      cameras: [], machines: [], users: []})
  const query = new URLSearchParams(window.location.search);
  let group_id = query.get("group_id");
  let caller = () => null;
  if (group_id !== null) {
    caller = callApiInto("get_group", setGroup, {group_id: Number(group_id)});
  }
  useEffect(caller, []);
  
  const [descriptionTab, name, descr] = DescriptionTab(group);
  
  const [machinesTab, machines] = AppendableList(
    setter => callApiInto("list_resources", setter, {resource_type: "machine"}),
    group.machines,
    machine => `${machine.name} (aruco: ${machine.aruco_id})`
  )
  const [camerasTab, cameras] = AppendableList(
    setter => callApiInto("list_resources", setter, {resource_type: "camera"}),
    group.cameras,
    camera => `${camera.name} (connection type: ${camera.connection})`
  )
  const [usersTab, users] = AppendableList(
    setter => callApiInto("list_users", setter),
    group.users,
    user => `${user.username} (${user.email})`
  )
  
  let nav = useNavigate();
  
  return (
    <>
      <Tab panes={[
        createPane('Description', descriptionTab),
        createPane('Machines', machinesTab),
        createPane('Cameras', camerasTab),
        createPane('Users', usersTab),
      ]}/>
      
      <Button primary
              content="Save"
              onClick={() => {
                callDbApi("modify_group", {
                  group_id: group_id,
                  name: name,
                  description: descr,
                  machines: toIds(machines),
                  cameras: toIds(cameras),
                  users: toIds(users),
                }).then(response => nav(`/modifygroup?group_id=${response.data.id}`));
              }}
      /> 
    </>
  )
}
