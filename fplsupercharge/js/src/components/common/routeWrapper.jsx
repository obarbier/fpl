import React from 'react';
import { Route, Switch, Redirect } from "react-router-dom"
import { componentsRoutes } from "./routes.jsx"
export default class RouteWrapper extends React.Component {
    render() {
        return (
            <Switch>
                {/* TODO: Need to find better way for default Route  catch all into redict*/}
             <Route
                exact
                path="/"
                render={() => {
                    return (<Redirect to="/teams" /> 
                        )
                      
                }}
              />
                {componentsRoutes.map((row, id) => {
                    return <Route
                        exact
                        key={row.key}
                        path={row.path}
                        children={<row.component />}
                    />
                })}
            </Switch>
        )
    }
}