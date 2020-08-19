import React, { Component } from 'react'
import {AgGridReact} from '@ag-grid-community/react';
import {TeamCellRender} from './agGridFramework'
import {ModuleRegistry} from '@ag-grid-community/core';
import {ClientSideRowModelModule} from '@ag-grid-community/client-side-row-model';
import {CsvExportModule} from "@ag-grid-community/csv-export";
import '@ag-grid-community/core/dist/styles/ag-grid.css';
import '@ag-grid-community/core/dist/styles/ag-theme-alpine.css';
ModuleRegistry.registerModules([ClientSideRowModelModule, CsvExportModule]);

class AgGridWrapper extends Component {
    constructor(props){
        super (props)
        this.state= {
            modules: [ClientSideRowModelModule ,CsvExportModule],
            columnDefs : [],
            rowData : [],
            style : {
                height: '800px',
                width: '100%'
            },
            frameworkComponents: {
                teamCellRender: TeamCellRender,
              },
            defaultColDef: {
                width: 150,
                resizable: false,
              },
        };
    }

    static getDerivedStateFromProps(nextProps) {

        const {
            columnDefs,
            rowData,
        } = nextProps;

        return {
            columnDefs,
            rowData,
        };

    }
    onGridReady = params => {
        this.gridApi = params.api;
        this.gridColumnApi = params.columnApi;
        this.gridApi.sizeColumnsToFit()
    }
    render() {
        const {
            columnDefs,
            rowData,
        } = this.state;

        return (
            <div style={{ width: '100%', height: '100%' }}>
            <div
            className="ag-theme-alpine agGrid"
            style={this.state.style}

          >
              <br/>
              <br/>

            <AgGridReact
                modules={this.state.modules}
                columnDefs={columnDefs}
                defaultColDef={this.state.defaultColDef}
                frameworkComponents={this.state.frameworkComponents}
                onGridReady={this.onGridReady}
                rowData={rowData}
            />
            </div>
            </div>
        );
    }
}

export default AgGridWrapper;