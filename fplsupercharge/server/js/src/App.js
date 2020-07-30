import React, { Component } from 'react';
import Navbar from "./components/navbar.jsx"
import './App.css';
import { BrowserRouter as Router} from "react-router-dom"
import { sideBarRoutes} from "./components/common/routes.jsx"
import RouteWrapper from "./components/common/routeWrapper"
// const USER_SERVICE_URL = "https://b74bd94e-5c37-45d8-9f4c-f707774dc21b.mock.pstmn.io/api/2.0/";
class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isFetching: false,
      teams: null,
      sidebar: sideBarRoutes
    };
  }

  componentDidMount() {

  }
  render() {
    return (
      <div className="container container--fluid ">
        <div className="container__row">
          <Router>
            <div className="container__col-2">
              <Navbar routes={this.state.sidebar} />
            </div>
            <div className="container__col-10 content">
                <RouteWrapper />
            </div>
          </Router>
        </div>
      </div>

    );
  }
}

export default App;