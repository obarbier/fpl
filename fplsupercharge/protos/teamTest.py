import unittest
from team_pb2 import team


class Teamtest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(Teamtest, self).__init__(*args, **kwargs)
        self.teamObject = team()
        self.teamObject.code = 3
        self.teamObject.draw = 0
        self.teamObject.form = 1
        self.teamObject.id = 1
        self.teamObject.loss = 0
        self.teamObject.name = "Arsenal"
        self.teamObject.played = 0
        self.teamObject.points = 0
        self.teamObject.position = 0
        self.teamObject.short_name = "ARS"
        self.teamObject.strength = 4
        self.teamObject.team_division = 1
        self.teamObject.unavailable = False
        self.teamObject.win = 0
        self.teamObject.strength_overall_home = 1180
        self.teamObject.strength_overall_away = 1240
        self.teamObject.code = 3
        self.teamObject.draw = 0
        self.teamObject.form = 1
        self.teamObject.id = 1
        self.teamObject.loss = 0
        self.teamObject.name = "Arsenal"
        self.teamObject.played = 0
        self.teamObject.points = 0
        self.teamObject.position = 0
        self.teamObject.short_name = "ARS"
        self.teamObject.strength = 4
        self.teamObject.team_division = 1
        self.teamObject.unavailable = False
        self.teamObject.win = 0
        self.teamObject.strength_overall_home = 1180
        self.teamObject.strength_overall_away = 1240
        self.teamObject.strength_attack_home = 1170
        self.teamObject.strength_attack_away = 1170
        self.teamObject.strength_defence_home = 1150
        self.teamObject.strength_defence_away = 1200
        self.teamObject.pulse_id = 1
        self.teamObject.strength_attack_home = 1170
        self.teamObject.strength_attack_away = 1170
        self.teamObject.strength_defence_home = 1150
        self.teamObject.strength_defence_away = 1200
        self.teamObject.pulse_id = 1

    def test_initialize(self):
        self.assertTrue(self.teamObject.IsInitialized())

    def test_object_create(self):
        self.assertTrue(isinstance(self.teamObject, team))


if __name__ == '__main__':
    unittest.main()
