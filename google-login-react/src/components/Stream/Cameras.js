import React, { useState, useEffect } from "react";
import { Image } from 'semantic-ui-react';

import {BACKEND_URL} from '../../App';

export default function Cam(cameras) {
  const [selected, setSelected] = useState({name : "", id : -1});
  useEffect(
    () => {
      if (cameras.length)
        setSelected(cameras[0]);
    },
    [cameras]
  );
  
  const [src, setSrc] = useState("");
  
  
  useEffect(() => setSrc(`${BACKEND_URL}/video_feed/${selected.id}`), [selected])
  
  return (
    <div>
        <Image
          src={src}
          alt="Video"
        />
    </div>
  )
};