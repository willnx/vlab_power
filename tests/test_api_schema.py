# -*- coding: UTF-8 -*-
"""
A suite of tests for the HTTP API schemas
"""
import unittest

from jsonschema import Draft4Validator, validate, ValidationError
from vlab_power_api.lib.views import power


class TestPowerViewSchema(unittest.TestCase):
    """A set of tes cases for the schemas in /api/1/inf/power end points"""

    def test_post_schema(self):
        """The schema defined for POST on /api/1/inf/power is a valid schema"""
        try:
            Draft4Validator.check_schema(power.PowerView.POST_SCHEMA)
            schema_valid = True
        except RuntimeError:
            schema_valid = False

        self.assertTrue(schema_valid)

    def test_post_schema_on(self):
        """Sending {"power": "on"} is valid input"""
        body = {"machine": "someMachine", "power": "on"}
        try:
            validate(body, power.PowerView.POST_SCHEMA)
            ok = True
        except ValidationError:
            ok = False

        self.assertTrue(ok)

    def test_post_schema_off(self):
        """Sending {"power": "off"} is valid input"""
        body = {"machine": "someMachine", "power": "off"}
        try:
            validate(body, power.PowerView.POST_SCHEMA)
            ok = True
        except ValidationError:
            ok = False

        self.assertTrue(ok)

    def test_post_schema_restart(self):
        """Sending {"power": "restart"} is valid input"""
        body = {"machine": "someMachine", "power": "restart"}
        try:
            validate(body, power.PowerView.POST_SCHEMA)
            ok = True
        except ValidationError:
            ok = False

        self.assertTrue(ok)

    def test_post_schema_junk(self):
        """Sending {"power": "asdfds"} is not valid input"""
        body = {"machine": "someMachine", "power": "asdfds"}
        try:
            validate(body, power.PowerView.POST_SCHEMA)
            ok = False
        except ValidationError:
            ok = True

        self.assertTrue(ok)

    def test_post_power_required(self):
        """Omitting the power object is invalid schema"""
        body = {"machine": "someMachine"}
        try:
            validate(body, power.PowerView.POST_SCHEMA)
            ok = False
        except ValidationError:
            ok = True

        self.assertTrue(ok)

    def test_post_machine_required(self):
        """Sending {"power": "asdfds"} is not valid input"""
        body = {"power": "on"}
        try:
            validate(body, power.PowerView.POST_SCHEMA)
            ok = False
        except ValidationError:
            ok = True

        self.assertTrue(ok)


if __name__ == '__main__':
    unittest.main()
