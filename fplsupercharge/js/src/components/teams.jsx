import React, { Component } from 'react'
import AgGridWrapper from './common/agGridWrapper';
import {fetchListOfTeams} from '../apiServices'
// import {teamCellRender} from '../utils'
import 'ag-grid-community/dist/styles/ag-grid.css';
import 'ag-grid-community/dist/styles/ag-theme-alpine.css';
// TODO: Add fixture details
export default class teams extends Component {
    constructor(props) {
        super(props);
        this.state = {
          columnDefs: [
            { headerName: 'Team', field: 'name',
              pinned: 'left',
            cellRenderer: 'teamCellRender',
            valueGetter: function(params) {
              var data = {'name': params.data.name,
                          'id':params.data.id,
                          'code':params.data.code}
              return data;
            },},
            { headerName: 'Points', field: 'points'},
            { headerName: 'Match Played', field: 'played'},    
            { headerName: 'Win', field: 'win'},
            { headerName: 'Draw', field: 'draw'},
            { headerName: 'Loss', field: 'loss'},
            { headerName: 'S.O.H.', field: 'strength_overall_home'},
            { headerName: 'S.O.A.', field: 'strength_overall_away'},
            { headerName: 'S.A.H.', field: 'strength_attack_home'},
            { headerName: 'S.A.A.', field: 'strength_attack_away'},
            { headerName: 'S.D.H.', field: 'strength_defence_home'},
            { headerName: 'S.D.A.', field: 'strength_defence_away'}
            ],
          rowData: []
        }
      }

    componentDidMount() {
      fetchListOfTeams()
      .then(data=>{
        this.setState({rowData:data.team })
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