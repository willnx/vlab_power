# -*- coding: UTF-8 -*-
"""
Unittest for the RESTful API of /api/1/inf/power end point
"""
import unittest
from unittest.mock import patch, MagicMock

from flask import Flask
from vlab_api_common.http_auth import generate_v2_test_token

import vlab_power_api.app as power_app
from vlab_power_api.lib.views import power


class TestPowerView(unittest.TestCase):
    """Test suite for PowerView"""

    @classmethod
    def setUpClass(cls):
        """Runs once, before any test case"""
        cls.token = generate_v2_test_token(username='bob')

    @classmethod
    def setUp(cls):
        app = Flask(__name__)
        power.PowerView.register(app)
        power_app.app.config['TESTING'] = True
        cls.app = app.test_client()
        # Mock Celery
        app.celery_app = MagicMock()
        cls.fake_task = MagicMock()
        cls.fake_task.id = 'asdf-asdf-asdf'
        app.celery_app.send_task.return_value = cls.fake_task

    def test_get(self):
        """GET on /api/1/inf/power without ?describe returns HTTP 400 response"""
        resp = self.app.get('/api/1/inf/power', headers={'X-Auth': self.token})
        expected = 400

        self.assertEqual(resp.status_code, expected)

    def test_post_task_id(self):
        """POST on /api/1/inf/power turns a task-id when givin valid input"""
        resp = self.app.post('/api/1/inf/power',
                             headers={'X-Auth': self.token},
                             json={'power': "on", "machine": "my VM"})

        result = resp.json['content']['task-id']
        expected = 'asdf-asdf-asdf'

        self.assertEqual(result, expected)

    def test_post_task_link(self):
        """POST on /api/1/inf/power sets the Link header"""
        resp = self.app.post('/api/1/inf/power',
                             headers={'X-Auth': self.token},
                             json={'power': "on", "machine": "my VM"})

        task_id = resp.headers['Link']
        expected = '<https://localhost/api/1/inf/power/task/asdf-asdf-asdf>; rel=status'

        self.assertEqual(task_id, expected)


if __name__ == '__main__':
    unittest.main()
