import React, { useState, useEffect } from "react";
import { Dropdown, Image } from 'semantic-ui-react';
import ReactPlayer from 'react-player'
import { config } from "../../utils";

import {BACKEND_URL} from '../../App';

function CameraSelector(cameras) {
  const [selected, setSelected] = useState({name : "", id : -1});
  useEffect(
    () => {
      if (cameras.length)
        setSelected(cameras[0]);
    },
    [cameras]
  );
  //onChange={(_, {value}) => setSelected(cameras.find(camera => camera.id === value))}
  let choice = cameras.map(camera => {return {key: camera.id, value: camera.id, text: camera.name}});
  return [(
    <Dropdown selection
              value={selected.id}
              text={selected.name}
              onChange={(_, {value}) => {setSelected(cameras.find(camera => camera.id === value))}}
              options={choice}
              />
  ), selected]
}

export default function Cam(cameras) {
  const [cameraSelector, camera] = CameraSelector(cameras);
  const [src, setSrc] = useState("");
  
  useEffect(() => setSrc(`${BACKEND_URL}/video_feed/${camera.id}`), [camera])
  
  return (
    <div>
      {cameraSelector}
        <Image
          src={src}
          alt="Video"
        />
    </div>
  )
};