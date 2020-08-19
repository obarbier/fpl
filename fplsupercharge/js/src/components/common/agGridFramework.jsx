import React, { Component } from 'react';
import {
    Link
  } from "react-router-dom";
export class TeamCellRender extends Component {

  render() {
    return (
        <span>
                <img className="flag" alt="" border="0" width="15" height="10" 
                src={"https://resources.premierleague.com/premierleague/badges/50/t" + this.props.value.code + ".png"}/>
                <Link to={"/team/"+this.props.value.id}>{this.props.value.name}</Link>
        </span>
        )
  }
}