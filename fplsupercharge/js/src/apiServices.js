import 'react'

const API_URL = "http://0.0.0.0:5000/api/2.0"

export const fetchListOfTeams= ()=>{
    return fetch(API_URL+"/fpl/listTeams")
    .then( (response) => {
        return response.json()
    })
}