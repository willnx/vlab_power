# -*- coding: UTF-8 -*-
"""
This module defines the API for working with auth tokens in vLab.
"""
from flask_classy import request
from vlab_inf_common.vmware import vCenter, vim
from vlab_api_common import BaseView, describe, get_logger, requires, validate_input


from vlab_power_api.lib import const


logger = get_logger(__name__, loglevel=const.VLAB_POWER_LOG_LEVEL)


class PowerView(BaseView):
    """API end point for turning on, off, or restarting virtual machines"""
    route_base = '/api/1/inf/power'
    GET_SCHEMA = {"$schema": "http://json-schema.org/draft-04/schema#",
                  "description": "Return all the virtual machines a user owns"
                 }
    POST_SCHEMA = {"$schema": "http://json-schema.org/draft-04/schema#",
                   "type": "object",
                   "properties": {
                      "power" : {
                         "type": "enum",
                         "description": "Power on, off, or restart a virtual machine"
                       },
                       "machine" : {
                          "type": "string",
                          "description": "The name of the VM. Supply 'all' to apply the power state to every VM you own."
                       }
                   },
                   "required": [
                      "power"
                   ]
                 }

    @describe(post=POST_SCHEMA)
    def get(self):
        """Only here to support the descript parameter"""
        resp = {'user' : username}
        status = 200
        return ujson.dumps(resp), status

    @requires(verify=True)
    @validate_input(schema=POST_SCHEMA)
    def post(self, *args, **kwargs):
        """Change the power state of a given virtual machine"""
        username = kwargs['token']['username']
        resp = {"user" : username}
        machine = kwargs['body']['virtual-machine']
        power = kwargs['body']['power']
        task = current_app.celery_app.send_task('power.modify', [username, power, machine])
        resp['content'] = {'task-id': task.id}
        return ujson.dumps(resp), 200
