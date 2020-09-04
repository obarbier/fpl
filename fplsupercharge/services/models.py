from protos.apiServices_pb2 import Team, Player
from utils.protosUtils import (node_creator
                               )
TEAM = node_creator(Team)
PLAYER = node_creator(Player)
