import React, { Component } from 'react'
import AgGridWrapper from './common/agGridWrapper';
import { fetchListOfTeams } from '../apiServices'
import 'ag-grid-community/dist/styles/ag-grid.css';
import 'ag-grid-community/dist/styles/ag-theme-alpine.css';
// TODO: Add fixture details
export default class teams extends Component {
  constructor(props) {
    super(props);
    this.state = {
      columnDefs: [
        {
          headerName: 'Team', field: 'name',
          pinned: 'left',
          cellRenderer: 'teamCellRender',
          valueGetter: function (params) {
            var data = {
              'name': params.data.name,
              'id': params.data.id,
              'code': params.data.code
            }
            return data;
          },
        },
        {
          headerName: 'Fixture', field: 'fixture',
          pinned: 'left',
          cellRenderer: 'fixtureCellRender',
        },
        {
          headerName: 'Points',
          valueGetter: (params) => { return params.data.points ? params.data.points : 0 },
          field: 'points'
        },
        {
          headerName: 'Match Played',
          valueGetter: (params) => { return params.data.played ? params.data.played : 0 },
          field: 'played'
        },
        {
          headerName: 'Win',
          valueGetter: (params) => { return params.data.win ? params.data.win : 0 },
          field: 'win'
        },
        {
          headerName: 'Draw',
          valueGetter: (params) => { return params.data.draw ? params.data.draw : 0 },
          field: 'draw'
        },
        {
          headerName: 'Loss',
          valueGetter: (params) => { return params.data.loss ? params.data.loss : 0 },
          field: 'loss'
        },
        { headerName: 'S.O.H.', field: 'strength_overall_home' },
        { headerName: 'S.O.A.', field: 'strength_overall_away' },
        { headerName: 'S.A.H.', field: 'strength_attack_home' },
        { headerName: 'S.A.A.', field: 'strength_attack_away' },
        { headerName: 'S.D.H.', field: 'strength_defence_home' },
        { headerName: 'S.D.A.', field: 'strength_defence_away' }
      ],
      rowData: []
    }
  }

  componentDidMount() {
    fetchListOfTeams()
      .then(data => {
        this.setState({ rowData: data.team })
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