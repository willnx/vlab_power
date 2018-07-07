# -*- coding: UTF-8 -*-
from flask import Flask
from celery import Celery

from vlab_power_api.lib import const
from vlab_power_api.lib.views import PowerView, HealthView

app = Flask(__name__)
app.celery_app = Celery('power', backend='rpc://', broker=const.VLAB_MESSAGE_BROKER)

HealthView.register(app)
PowerView.register(app)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
