import React, { Component } from 'react'
import AgGridWrapper from './common/agGridWrapper';
import {fetchListOfTeams} from '../apiServices'
import 'ag-grid-community/dist/styles/ag-grid.css';
import 'ag-grid-community/dist/styles/ag-theme-alpine.css';
export default class teams extends Component {
    constructor(props) {
        super(props);
        this.state = {
          columnDefs: [],
          rowData: []
        }
      }

    componentDidMount() {
      fetchListOfTeams()
      .then(data=>{
        data = this.setState({columnDefs:data.columnDefs,rowData:data.rowData })
      })
    }
    render() {
        return (
            <AgGridWrapper
              columnDefs={this.state.columnDefs}
              rowData={this.state.rowData}>
            </AgGridWrapper>
        );
      }
    }