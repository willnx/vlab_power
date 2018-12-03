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
from vlab_api_common import get_task_logger
from vlab_inf_common.vmware import vCenter, virtual_machine, vim

from vlab_power_api.lib import const

app = Celery('power', backend='rpc://', broker=const.VLAB_MESSAGE_BROKER)


@app.task(name='power.modify', bind=True)
def modify(self, username, power_state, machine, txn_id):
    """Celery task for changing the power state of Virtual Machine(s)

    :Returns: Dictionary

    :param username: The name of the user who owns the supplied VM(s)
    :type username: String

    :param power_state: The desired power state for the supplied VM(s)
    :type power_state: String

    :param machine: The name of the VM(s) to power on/off/restart
    :type machine: String

    :param txn_id: A unique string supplied by the client to track the call through logs
    :type txn_id: String
    """
    logger = get_task_logger(txn_id=txn_id, task_id=self.request.id, loglevel=const.VLAB_POWER_LOG_LEVEL.upper())
    resp = {'content' : {}, 'error' : None, 'params' : {'power': power_state, 'machine': machine}}
    logger.info('Task Starting')
    try:
        modify_power(username, power_state, machine, logger)
    except ValueError as doh:
        err = '{}'.format(doh)
        logger.info('Task Failure: {}'.format(err))
        resp['error'] = '{}'.format(err)
    logger.info('Task Completed')
    return resp


def modify_power(username, power_state, machine, logger):
    """Keeps business logic out of Celery task

    :Returns: None

    :Raises: ValueError, RuntimeError

    :param username: The name of the user who owns the supplied VM(s)
    :type username: String

    :param power_state: The desired power state for the supplied VM(s)
    :type power_state: String

    :param machine: The name of the VM(s) to power on/off/restart
    :type machine: String

    :param logger: An object for logging messages
    :type logger: logging.LoggerAdapter
    """
    with vCenter(host=const.INF_VCENTER_SERVER, user=const.INF_VCENTER_USER, \
                 password=const.INF_VCENTER_PASSWORD) as vcenter:
        folder = vcenter.get_by_name(name=username, vimtype=vim.Folder)
        vms = [x for x in folder.childEntity]

        logger.debug('All user VMS: {}'.format(','.join([x.name for x in vms])))
        if machine.lower() != 'all':
            vms = [x for x in vms if x.name == machine]
        if not vms:
            error = 'No machine named {} found'.format(machine)
            raise ValueError(error)

        errors = []
        debug_msg = 'VM(s) getting power state adjusted to {}: {}'.format(','.join([x.name for x in vms]),
                                                                          power_state)
        logger.debug(debug_msg)
        for vm in vms:
            ok = virtual_machine.power(vm, power_state)
            if not ok:
                msg = 'Unable to power {} {}'.format(power_state, vm.name)
                errors.append(msg)
        if errors:
            msg = ', '.join(errors)
            raise RuntimeError(msg)
