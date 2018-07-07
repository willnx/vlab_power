# -*- coding: UTF-8 -*-
"""
Enables Health checks for the power API
"""
from time import time
import pkg_resources

import ujson
from flask_classy import FlaskView, Response
from vlab_inf_common.vmware import vCenter

from vlab_power_api.lib import const


class HealthView(FlaskView):
    """
    Simple end point to test if the service is alive
    """
    route_base = '/api/1/inf/power/healthcheck'
    trailing_slash = False

    def get(self):
        """End point for health checks"""
        resp = {}
        status = 200
        stime = time()
        try:
            with vCenter(host=const.INF_VCENTER_SERVER, user=const.INF_VCENTER_USER,
                         password=const.INF_VCENTER_PASSWORD, verify=const.INF_VCENTER_VERIFY_CERT):
                pass
        except Exception as doh:
            resp['error'] = '{}'.format(doh)
            status = 500
        else:
            resp['error'] = None
        resp['latency'] = time() - stime

        resp['version'] = pkg_resources.get_distribution('vlab-power-api').version
        response = Response(ujson.dumps(resp))
        response.status_code = status
        response.headers['Content-Type'] = 'application/json'
        return response
