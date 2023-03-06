import React, { useEffect, useState } from 'react';
import { Button, Input, Form, Tab, TextArea, List, Dropdown, Container } from 'semantic-ui-react';

import { callApiInto } from '../utils';

function makeStrNonEmpry(str) {
  return str === ""? " " : str;
}

export default function ModifyGroup() {
  const [result, setResult] = useState({});
  const [command, setCommand] = useState("");
  const [args, setArgs] = useState("{}");
  const [button, setButton] = useState(null);
  
  useEffect(() =>{
    try {
      let argsParsed = JSON.parse(args);
      setButton(<Button primary
                       content="Send"
                       onClick={callApiInto(command, setResult, argsParsed)}/>);
    } catch (err) {
      setButton(<Button disabled content="Bad JSON"/>);
      return;
    }
  }, [args, command]);
  
  return (
    <>
      <Container text>
        <Form>
          <Form.Field name='name'
                      control={Input}
                      value={command}
                      label='command'
                      onChange={(e, { value }) => setCommand(value)}
          />
          
          <Form.Field name='description'
                      control={TextArea}
                      value={args}
                      label='data to send (json)'
                      onChange={(e, { value }) => setArgs(makeStrNonEmpry(value))}
          />
        </Form>
        
        {button}
        <h5>Result:</h5><br/>
        <p>{JSON.stringify(result, null, 2)}</p>
      </Container>
    </>
  )
}
