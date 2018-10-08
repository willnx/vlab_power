# -*- coding: UTF-8 -*-
"""
This module defines the API for working with auth tokens in vLab.
"""
import ujson
from flask import current_app
from flask_classy import request, Response
from vlab_inf_common.views import TaskView
from vlab_inf_common.vmware import vCenter, vim
from vlab_api_common import describe, get_logger, requires, validate_input


from vlab_power_api.lib import const


logger = get_logger(__name__, loglevel=const.VLAB_POWER_LOG_LEVEL)


class PowerView(TaskView):
    """API end point for turning on, off, or restarting virtual machines"""
    route_base = '/api/1/inf/power'
    GET_SCHEMA = {"$schema": "http://json-schema.org/draft-04/schema#",
                  "description": "Return all the virtual machines a user owns"
                 }
    POST_SCHEMA = {"$schema": "http://json-schema.org/draft-04/schema#",
                   "type": "object",
                   "properties": {
                      "power" : {
                         "oneOf": [
                            {"type": "string", "pattern": "on"},
                            {"type": "string", "pattern": "off"},
                            {"type": "string", "pattern": "restart"}
                         ],
                         "description": "Power on, off, or restart a virtual machine"
                       },
                       "machine" : {
                          "type": "string",
                          "description": "The name of the VM. Supply 'all' to apply the power state to every VM you own."
                       }
                   },
                   "required": [
                      "power",
                      "machine"
                   ]
                 }

    @describe(post=POST_SCHEMA)
    @requires(verify=False, version=(1,2))
    def get(self, *args, **kwargs):
        """Only here to support the describe parameter"""
        username = kwargs['token']['username']
        resp = {'user' : username, 'error': "End point only supports the user of the describe parameter"}
        status = 400
        return ujson.dumps(resp), status

    @requires(verify=False, version=(1,2))
    @validate_input(schema=POST_SCHEMA)
    def post(self, *args, **kwargs):
        """Change the power state of a given virtual machine"""
        username = kwargs['token']['username']
        resp_data = {"user" : username}
        machine = kwargs['body']['machine']
        power = kwargs['body']['power']
        task = current_app.celery_app.send_task('power.modify', [username, power, machine])
        resp_data['content'] = {'task-id': task.id}
        resp = Response(ujson.dumps(resp_data))
        resp.status_code = 202
        resp.headers.add('Link', '<{0}{1}/task/{2}>; rel=status'.format(const.VLAB_URL, self.route_base, task.id))
        return resp
