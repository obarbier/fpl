import React, { Component } from 'react';
import { NavLink } from "react-router-dom";
import { Chevron } from "./common/svg";

export default class NavbarList extends Component {
    constructor(props) {
        super(props)
        this.state = {
            showChildrenTag: false
        };
        this.toggleChild = this.toggleChild.bind(this)
    }

    toggleChild(event) {
        event.preventDefault()
        this.setState({ showChildrenTag: !this.state.showChildrenTag })
    }

    render() {
        return (
            <>
                <li>
                    <NavLink activeClassName="active-route" to={this.props.route.path}>{this.props.route.name}</NavLink>
                    {this.props.route.hasChildren &&
                        <button className="btn-toggle" onClick={this.toggleChild}>
                            <Chevron className={this.state.showChildrenTag ? "rotate" : ""} height={16} width={16} fill={"#777"} />
                        </button>
                    }
                </li>
                <ul className={this.state.showChildrenTag ? "" : "deactive"}>
                    {this.props.route.children.map((child, index) => {
                        return (
                            <li key={index}>
                                <NavLink activeClassName="active-route" to={child.path}>{child.name}</NavLink>
                            </li>
                        )
                    })}
                </ul>
            </>
        )
    }
}