#!/usr/bin/env python

"""Tests for `fplsupercharge` package."""


import unittest
import os
from click.testing import CliRunner

# from fplsupercharge import fplsupercharge
from fplsupercharge import cli
from fplsupercharge.Utils.iniFileConstant import SAVE_TEMPLATE, FILE_NAME

class TestFplsupercharge(unittest.TestCase):
    """Tests for `fplsupercharge` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_init_and_teardown(self):
        """Test something."""
        runner = CliRunner()
        args = "\n".join(["test@test.com","password","password","1","1","1","0.0.0.0:1234","password", "password" ,""])
        help_result = runner.invoke(cli.init, input =args)
        assert os.path.exists(SAVE_TEMPLATE.format(FILE_NAME)) == 1
        assert help_result.exit_code == 0
        #FIXME: Teardown
        # runner = CliRunner()
        # help_result = runner.invoke(cli.teardown, input ="\n")
        # print(help_result.output)
        # assert help_result.exit_code == 0
        # assert os.path.exists(SAVE_TEMPLATE.format(FILE_NAME)) == 0

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        # assert '--help  Show this message and exit.' in help_result.output
if __name__ == '__main__':
    unittest.main()
    