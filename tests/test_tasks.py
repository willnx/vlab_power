# -*- coding: UTF-8 -*-
"""
A suite of tests for the functions in tasks.py
"""
import unittest
from unittest.mock import patch, MagicMock

from vlab_power_api.lib.worker import tasks


class TestTasks(unittest.TestCase):
    """A set of test cases for tasks.py"""

    @patch.object(tasks, 'modify_power')
    def test_modify(self, fake_modify_power):
        """``modify`` returns a dictionary when everything works as expected"""
        result = tasks.modify(username='alice',
                              power_state='on',
                              machine='myVM')
        expected = {'content': {}, 'error': None, 'params': {'machine': 'myVM', 'power': 'on'}}

        self.assertEqual(result, expected)

    @patch.object(tasks, 'modify_power')
    def test_modify_value_error(self, fake_modify_power):
        """``modify`` catches ValueError"""
        fake_modify_power.side_effect = [ValueError('testing')]
        result = tasks.modify(username='alice',
                              power_state='on',
                              machine='myVM')
        expected = {'content': {}, 'error': 'testing', 'params': {'machine': 'myVM', 'power': 'on'}}

        self.assertEqual(result, expected)

    @patch.object(tasks.virtual_machine, 'power')
    @patch.object(tasks, 'vCenter')
    def test_modify_power(self, fake_vCenter, fake_power):
        """``modify_power`` returns None when everything works as expected"""
        fake_vm = MagicMock()
        fake_vm.name = 'myVM'
        fake_folder = MagicMock()
        fake_folder.childEntity = [fake_vm]
        fake_vCenter.return_value.__enter__.return_value.get_by_name.return_value = fake_folder

        output = tasks.modify_power(username='alice',
                                    power_state='on',
                                    machine='myVM')
        expected = None

        self.assertEqual(output, expected)

    @patch.object(tasks.virtual_machine, 'power')
    @patch.object(tasks, 'vCenter')
    def test_modify_power_no_vms(self, fake_vCenter, fake_power):
        """``modify_power`` raises ValueError if no VMs are found"""
        fake_vm = MagicMock()
        fake_vm.name = 'myVM'
        fake_folder = MagicMock()
        fake_folder.childEntity = [fake_vm]
        fake_vCenter.return_value.__enter__.return_value.get_by_name.return_value = fake_folder

        with self.assertRaises(ValueError):
            tasks.modify_power(username='alice',
                               power_state='on',
                               machine='NoVMs')

    @patch.object(tasks.virtual_machine, 'power')
    @patch.object(tasks, 'vCenter')
    def test_modify_power_failure(self, fake_vCenter, fake_power):
        """``modify_power`` raises RuntimeError if changing the power state fails"""
        fake_vm = MagicMock()
        fake_vm.name = 'myVM'
        fake_folder = MagicMock()
        fake_folder.childEntity = [fake_vm]
        fake_vCenter.return_value.__enter__.return_value.get_by_name.return_value = fake_folder
        fake_power.return_value = None

        with self.assertRaises(RuntimeError):
            tasks.modify_power(username='alice',
                               power_state='on',
                               machine='myVM')

if __name__ == '__main__':
    unittest.main()
