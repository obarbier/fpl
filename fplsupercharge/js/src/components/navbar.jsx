import React, { Component } from "react";
import NavbarList from "./navbarList"
export default class Navbar extends Component {
  constructor(props) {
    super(props);
    this.state = {routes: (this.props.routes !== undefined)? this.props.routes: []} 
  }
  componentDidMount() {

  }
  render() {
    return (
        <nav className="navbar">
          <div className="container__row">
            <div className="navbar__header container__col-12">
              <h3>Navbar</h3>
            </div>
          </div>
          <div className="container__row">
            <div className="navbar__body container__col-12">
              <ul>
              {this.state.routes.map((route,index)=>{
                return <NavbarList key={index} route={route} />
              })}
              </ul>
            </div>
          </div>
        </nav>
    );
  }
}

