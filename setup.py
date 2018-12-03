#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
RESTful endpoints for powering on/off/restarting VMs in vLab
"""
from setuptools import setup, find_packages


setup(name="vlab-power-api",
      author="Nicholas Willhite,",
      author_email='willnx84@gmail.com',
      version='2018.12.03',
      packages=find_packages(),
      include_package_data=True,
      package_files={'vlab_folder_api' : ['app.ini']},
      description="vLab service for powering on/off/restart VMs",
      install_requires=['flask', 'ldap3', 'pyjwt', 'uwsgi', 'vlab-api-common',
                        'ujson', 'cryptography', 'vlab-inf-common', 'celery']
      )
