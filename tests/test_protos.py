"""Tests for `fplsupercharge.protos` package."""

import unittest
from fplsupercharge.protos.team_pb2 import Team


class TestProtos(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures, if any."""
        self.teamObject = Team()
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

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_initialize(self):
        """Test_initialize Protos Teams."""
        self.assertTrue(self.teamObject.IsInitialized())
        self.assertTrue(isinstance(self.teamObject, Team))


if __name__ == '__main__':
    unittest.main()
