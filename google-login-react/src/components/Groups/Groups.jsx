import React, {useEffect, useState, useRef} from "react";
import { Table, Tab, Button, Accordion, Icon, Divider, Header, Container } from "semantic-ui-react";
import { callApiInto, isAdmin } from "../../utils";
import { Link, useLocation, useNavigate} from "react-router-dom";

import { renderList } from "./GroupModification";

function groupButton(group, nav) {
  if (isAdmin()) {
    return (
      <>
        <Button primary
                icon="settings"
                floated="right"
                onClick={() => nav(`/modifygroup?group_id=${group.id}`)}
        />
      </>
    )
  }
  
  return <></>
}
function addButton(nav) {
  if (isAdmin()) {
    return (
     <Button positive
             icon="plus"
             onClick={() => nav("/modifygroup")}/>
    )
  }
  return <></>
}

function Groups() {
  const [groups, setGroups] = useState([]);
  const [machines, setMachines] = useState([]);
  const [cameras, setCameras] = useState([]);
  
  useEffect(callApiInto("list_groups", setGroups), []);
  useEffect(callApiInto("list_resources", setMachines, {resource_type: "machine"}), []);
  useEffect(callApiInto("list_resources", setCameras, {resource_type: "camera"}), []);
  
  const nav = useNavigate();
  
  const [activeIndex, setActiveIndex] = useState([]);
  const handleClick = (_, {index}) => setActiveIndex(activeIndex === index? -1 : index)
  
  let accordion = (
    <Accordion fluid styled>
      {groups.map(group =>
        <div key={group.id}>
          <Accordion.Title active={activeIndex === group.id}
                           index={group.id}
                           onClick={handleClick}
          >
            <Accordion.Content>
              <Icon name='dropdown' />
              {group.name}
              <Button positive
                      content="connect"
                      floated="right"
                      onClick={() => nav(`/stream?group_id=${group.id}`)}
              />
              {groupButton(group, nav)}
            </Accordion.Content>
          </Accordion.Title>
          
          <Accordion.Content active={activeIndex === group.id}>
          <Header as='h4' content="Description"/>
          <p>{group.description}</p>
          <Divider hidden />

          <Header as='h4' content="Cameras"/>
          {renderList(cameras.filter(camera => group.cameras.includes(camera.id)),
                      camera => `${camera.name} (connection type: ${camera.connection})`)}
          <Divider hidden/>

          <Header as='h4' content="Machines"/>
          {renderList(machines.filter(machine => group.machines.includes(machine.id)),
                      machine => `${machine.name} (aruco: ${machine.aruco_id})`)}
          </Accordion.Content>
        </div>
      )}
    </Accordion>
  );
  
  return (
    <>
    { accordion }
    <Container textAlign='center'>
    {addButton(nav)}
    </Container>
    </>
  )
}

export default Groups;