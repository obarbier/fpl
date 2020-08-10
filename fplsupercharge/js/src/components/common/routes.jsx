import teams from "../teams.jsx";
import team from "../team.jsx";
export const sideBarRoutes = [
  {
    key:0,
    path: "/teams",
    name: "Teams",
    hasChildren: true,
    children:[{
      key:0,
      path: "/team/1",
      name: "Team1",
    },{
      key:1,
      path: "/team/2",
      name: "Team2",
    },{
      key:3,
      path: "/team/3",
      name: "Team3",
    }]

    
  }

]
export const componentsRoutes = [
    {
      key:0,
      path: "/teams",
      component: teams
    },
    {
      key:1,
      path: "/team/:id",
      component: team
    }
];