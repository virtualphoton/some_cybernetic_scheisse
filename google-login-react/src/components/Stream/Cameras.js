import React, { useState, useEffect } from "react";
import { Dropdown } from 'semantic-ui-react';
import ReactPlayer from 'react-player'
import { config } from "../../utils";

import {BACKEND_URL} from '../../App';

function CameraSelector(cameras) {
  const [selected, setSelected] = useState({name : "", id : -1});
  useEffect(
    () => cameras.size()? setSelected(cameras[0]) : null,
    [cameras]
  );
  
  return [(
    <Dropdown text={selected.name}
              value={selected.id}
              onChange={(_, {value}) => setSelected(cameras.find(camera => camera.id === value))}>
                
      <Dropdown.Menu>
        {cameras.map(camera =>
          <Dropdown.Item text={camera.name} key={camera.id}/>
        )}
      </Dropdown.Menu>
    </Dropdown>
  ), selected]
}

function Stream(camera) {
  const [url, setUrl] = useState()
  
  useEffect(() => {
    if (!camera)
      return;
    let cur_url = `${BACKEND_URL}/video_feed/${camera.id}`;
    fetch(cur_url, config())
      .then(response => response.blob())
        .then(blob => setUrl(URL.createObjectURL(blob)));
  }, [camera])
  
  return (
      <ReactPlayer url={url} width="100%" />
  )
};


function Cam(prop) {
  let cameras = prop.cameras;
  
  const [cameraSelector, camera] = CameraSelector(cameras);
  const stream = Stream(camera);
  
  return (
    <div>
      {cameraSelector}
      {stream}
    </div>
  )
};
  
export default Cam;