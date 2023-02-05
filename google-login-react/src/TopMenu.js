import React, { Component } from 'react'
import { Button, Menu, Dropdown } from 'semantic-ui-react'

export default class TopMenu extends Component {
  state = {}

  handleItemClick = (e, { name }) => this.setState({ activeItem: name })

  render() {
    const { activeItem } = this.state

    return (
      <Menu>
        <Menu.Item
          name='stream'
          active={activeItem === 'stream'}
          onClick={this.handleItemClick}
        >
          Stream
        </Menu.Item>

        <Menu.Item
          name='groups'
          active={activeItem === 'groups'}
          onClick={this.handleItemClick}
        >
          Groups
        </Menu.Item>
        
        <Menu.Item
          name='admin'
          active={activeItem === 'admin'}
        >
          <Dropdown text='Administrating'>
            <Dropdown.Menu>
              <Dropdown.Item name='admin' onClick={this.handleItemClick}>Resources</Dropdown.Item>
              <Dropdown.Item name='admin' onClick={this.handleItemClick}>Users</Dropdown.Item>
            </Dropdown.Menu>
          </Dropdown>
        </Menu.Item>
        
        <Menu.Item position='right'>
          <Button>Log-in</Button>
        </Menu.Item>
      </Menu>
    )
  }
}
