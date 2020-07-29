import React, { Component } from 'react'
import AgGridWrapper from './common/agGridWrapper';

import 'ag-grid-community/dist/styles/ag-grid.css';
import 'ag-grid-community/dist/styles/ag-theme-alpine.css';
export default class teams extends Component {
    constructor(props) {
        super(props);
        this.state = {
          columnDefs: [{
            headerName: "Make", field: "make"
          }, {
            headerName: "Model", field: "model"
          }, {
            headerName: "Price", field: "price"
          }],
          rowData: [{
            make: "Toyota", model: "Celica", price: 35000
          }, {
            make: "Ford", model: "Mondeo", price: 32000
          }, {
            make: "Porsche", model: "Boxter", price: 72000
          }]
        }
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