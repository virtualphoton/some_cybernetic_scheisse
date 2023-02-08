import React, { useEffect, useState } from 'react'
import { Button, Input, Form, Tab, TextArea, List, Dropdown } from 'semantic-ui-react'

import { callApiInto, callDbApi } from '../../utils';

function createPane(title, content) {
  return {
    menuItem: title,
    render: () => <Tab.Pane>{content}</Tab.Pane>
  };
}

function AppendableList(retrieve_all, selected_ids, repr) {
  const [all, setAll] = useState([]);
  const [selected, setSelected] = useState([]);
  const [unselectedList, setUnselected] = useState([]);
  
  useEffect(retrieve_all(setAll), []);
  useEffect(() => setSelected([...all].filter(item => selected_ids.includes(item.id))), [all]);
  useEffect(() => {
    let used_ids = selected.map(item => item.id);
    let unselected = [...all].filter(item => !used_ids.includes(item.id))
    setUnselected(unselected.map(
      item => {return {key: item.id, value: item.id, text: repr(item)}}
    ));
    console.log(selected);
  }, [selected]);
  
  function deleter(id) {
    return () => setSelected(selected.filter(item => item.id !== id));
  }
  return [(
    <List divided verticalAlign='middle'>
      {selected.map(item =>
        <List.Item key={item.id}>
          <List.Content floated='right'>
            <Button negative
                    icon="close"
                    onClick={deleter(item.id)}
            /> 
          </List.Content>
          
          <List.Content content={repr(item)}/>
        </List.Item>
      )}
      
      <Dropdown placeholder='Add new (Esc, to close selection)'
                search selection
                value={""}
                options={unselectedList}
                onChange={(_, {value}) => 
                  setSelected([...selected, all.find(item => item.id === value)])}
      />
    </List>
  ), selected];
}

function DescriptionTab(group) {
  const [name, setName] = useState(group.name);
  const [descr, setDescr] = useState(group.description);
  return [(
    <Form>
      <Form.Field name='name'
                  control={Input}
                  value={name}
                  label='Group name'
                  onChange={(e, { value }) => setName(value)}
                  inline
      />
      
      <Form.Field name='description'
                  control={TextArea}
                  value={descr}
                  label='Group name'
                  onChange={(e, { value }) => setDescr(value)}
      />
    </Form>
  ), name, descr]
}

export default function ModifyGroup() {
  const [group, setGroup] = useState({id: null, name: "", description: "",
                                      cameras: [], machine_specs: [], users: []})
  const query = new URLSearchParams(window.location.search);
  let group_id = query.get("group_id");
  if (group_id === null) {
    // TODO
  } else {
    //useEffect(callApiInto("get_group", setGroup, {group_id: Number()}), []);
  }
  
  const [descriptionTab, name, descr] = DescriptionTab(group);
  
  const [machinesTab, machines] = AppendableList(
    setter => callApiInto("list_resources", setter, {resource_type: "machine"}),
    group.machine_specs,
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
  
  const panes = [
    createPane('Description', descriptionTab),
    createPane('Machines', machinesTab),
    createPane('Cameras', camerasTab),
    createPane('Users', usersTab),
  ]
  
  const toIds = arr => arr.map(item => item.id);
  
  return (
    <>
      <Tab panes={panes} />
      <Button primary
              content="Save"
              onClick={() => callDbApi("update_group", {
                group_id: group_id,
                name: name, description: descr,
                machines: toIds(machines),
                cameras: toIds(cameras),
                users: toIds(users),
              })}
      /> 
    </>
  )
}
