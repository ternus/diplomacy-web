# -*- coding: utf-8 -*-
"""Setup the diplomacy application"""

import logging

from diplomacy.config.environment import load_environment

__all__ = ['setup_app']

log = logging.getLogger(__name__)

from schema import setup_schema
import bootstrap

def setup_app(command, conf, vars):
    """Place any commands to setup diplomacy here"""
    load_environment(conf.global_conf, conf.local_conf)
    setup_schema(command, conf, vars)
    bootstrap.bootstrap(command, conf, vars)
