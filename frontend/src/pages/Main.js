import React from "react";
import {TerminalContextProvider} from "react-terminal";
import Cam from "./Cam";
import Machines from "./Machines";
import Terminal from "./Terminal";
import styled from "styled-components";

const Flexed = styled.div`
  display: flex;
  justify-content: flex-start;
`

function Main() {
  return (
    <TerminalContextProvider>
      <Flexed>
        <Cam/>
        <Machines/>
      </Flexed>
      <Terminal/>
    </TerminalContextProvider>
  )
}

export default Main;
