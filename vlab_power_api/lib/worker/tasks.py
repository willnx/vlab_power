# -*- coding: UTF-8 -*-
"""
This module defines all tasks for creating, deleting, listing virtual vLANs.

All responses from a task *MUST* be a dictionary, and *MUST* contain the following
keys:

- ``error``  An error message about bad user input,or None
- ``params`` The parameters provided by the user, or an empty dictionary
- ``content`` The resulting output from running a task, or an empty dictionary

Example:

.. code-block:: python

   # If everything works
   {'error' : None,
    'content' : {'vlan' : 24, 'name': 'bob_FrontEnd'}
    'params' : {'vlan-name' : 'FrontEnd'}
   }
   # If bad params are provided
   {'error' : "Valid parameters are foo, bar, baz",
    'content' : {},
    'params' : {'doh': 'Not a valid param'}
   }

"""
from celery import Celery
from vlab_api_common import get_logger
from vlab_inf_common.vmware import vCenter

from vlab_power_api.lib import const

app = Celery('power', backend='rpc://', broker=const.VLAB_MESSAGE_BROKER)
logger = get_logger(__name__, loglevel=const.VLAB_POWER_LOG_LEVEL)


@app.task(name='power.modify')
def modify(username, power, machine):
    """TODO"""
    resp = {'content' : {}, 'error' : None, 'params' : {'power': power, 'machine': machine}}
    # TODO change the thingies
