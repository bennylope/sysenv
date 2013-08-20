#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Ben Lopatin'
__email__ = 'ben@wellfire.co'
__version__ = '0.1.0'

import os
import re
import logging

from .data import EnvDict


logger = logging.getLogger(__name__)


def read_file_values(env_file, fail_silently=True):
    """
    Borrowed from Honcho
    """
    env_data = {}
    try:
        with open(env_file) as f:
            content = f.read()
    except IOError:
        if fail_silently:
            logging.error("Could not read file '{0}'".format(env_file))
            return env_data
        raise

    for line in content.splitlines():
        m1 = re.match(r'\A([A-Za-z_0-9]+)=(.*)\Z', line)
        if m1:
            key, val = m1.group(1), m1.group(2)

            m2 = re.match(r"\A'(.*)'\Z", val)
            if m2:
                val = m2.group(1)

            m3 = re.match(r'\A"(.*)"\Z', val)
            if m3:
                val = re.sub(r'\\(.)', r'\1', m3.group(1))

            env_data[key] = val

    return env_data


def load(env_file=None, fail_silently=True, load_globally=True, **kwargs):
    """
    Returns an instance of EnvDict after reading the system environment an
    optionally provided file.
    """
    data = {}
    data.update(os.environ)
    if env_file:
        data.update(read_file_values(env_file, fail_silently))
    if load_globally:
        os.environ.update(data)
    return EnvDict(data, **kwargs)
