#!/usr/bin/env python
# -*- coding: utf-8 -*-

from decimal import Decimal

# TODO open this to translation/expansion?
TRUE_VALUES = ('true', 'on', 'yes', '1')


class EnvDict(dict):
    """
    A dictionary that starts from a system environment dictionary and casts
    dictionary values from source strings.
    """

    def __init__(self, *args, **kwargs):
        """
        Pull in the default environment variables, then update using a provided
        file, then update with the first
        """
        self.cast_funcs = {
            int: int,
            str: str,
            float: float,
            bool: lambda x: x.lower() in TRUE_VALUES,
            list: lambda x: list(x.split(',')),
            dict: lambda x: dict([y.split('=') for y in x.split(',')]),
            'decimal': lambda x: Decimal(x),
        }
        self.cast_funcs.update(kwargs.pop('casts', {}))
        self.schema = kwargs.pop('schema', {})
        super(EnvDict, self).__init__(*args, **kwargs)
        for key, cast in self.schema.items():
            self[key] = self.cast_funcs.get(cast, str)(self[key])

    def get(self, key, default=None, **kwargs):
        """
        The default value should never be cast
        """
        cast = kwargs.pop('cast', None)

        if not key in self:
            return default
        val = self[key]

        if cast is not None:
            return self.cast_funcs.get(cast, str)(val)
        return val

    def pop(self, key, default=None, **kwargs):
        """
        The default value should never be cast
        """
        cast = kwargs.pop('cast', None)

        if not key in self:
            return default
        val = self[key]

        if cast is not None:
            return self.cast_funcs.pop(cast, str)(val)
        return val

    def recast(self, schema=None):
        """
        Should recast the dictionary based on a schema
        """
        if schema:
            self.schema = schema
        for key, cast in self.schema.items():
            self[key] = self.cast_funcs.get(cast, str)(self[key])
        return self
