#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest
from decimal import Decimal

from sysenv import load, read_file_values
from sysenv.data import EnvDict


class TestEnvDict(unittest.TestCase):
    """
    Tests that the EnvDict class casts string values provided a schema of
    specified types
    """

    def test_boolean_cast(self):
        self.assertTrue(EnvDict({'DEBUG': 'True'}, schema={'DEBUG': bool})['DEBUG'])
        self.assertTrue(EnvDict({'DEBUG': 'true'}, schema={'DEBUG': bool})['DEBUG'])
        self.assertTrue(EnvDict({'DEBUG': 'on'}, schema={'DEBUG': bool})['DEBUG'])
        self.assertTrue(EnvDict({'DEBUG': '1'}, schema={'DEBUG': bool})['DEBUG'])
        self.assertFalse(EnvDict({'DEBUG': 'False'}, schema={'DEBUG': bool})['DEBUG'])
        self.assertFalse(EnvDict({'DEBUG': 'off'}, schema={'DEBUG': bool})['DEBUG'])
        self.assertFalse(EnvDict({'DEBUG': 'debug'}, schema={'DEBUG': bool})['DEBUG'])

    def test_decimal_cast(self):
        self.assertTrue(isinstance(EnvDict({'DECIMAL': '1'}, schema={'DECIMAL': 'decimal'})['DECIMAL'], Decimal))

    def test_float_cast(self):
        self.assertTrue(isinstance(EnvDict({'FLOAT': '1'}, schema={'FLOAT': float})['FLOAT'], float))

    def test_list_cast(self):
        self.assertTrue(isinstance(EnvDict({'MYLIST': '1'}, schema={'MYLIST': list})['MYLIST'], list))

    def test_dict_cast(self):
        self.assertTrue(isinstance(EnvDict({'SOMEDICT': 'a=a,name=tester'}, schema={'SOMEDICT': dict})['SOMEDICT'], dict))

    def test_missing_cast_cast(self):
        """Missing cast should default to a string"""
        self.assertTrue(isinstance(EnvDict({'DEBUG': '1'}, schema={'DEBUG': 'kjkjdjk'})['DEBUG'], str))

    def test_missing_key(self):
        """Ensure the defaults work as expected"""
        self.assertTrue(EnvDict({}).get('DEBUG', True))
        self.assertFalse(EnvDict({}).get('DEBUG', False))

    def test_cast_get_method(self):
        """Ensure that the get method can cast"""
        envdict = EnvDict({'DEBUG': '1'})
        self.assertEqual(True, envdict.get('DEBUG', cast=bool))
        self.assertEqual(True, envdict.get('MISSING', True, cast=bool))
        self.assertEqual('True', envdict.get('MISSING', 'True', cast=bool))

    def test_cast_pop_method(self):
        """Ensure that the pop method can cast"""
        envdict = EnvDict({'DEBUG': '1'})
        self.assertEqual(True, envdict.pop('DEBUG', cast=bool))
        self.assertEqual(True, envdict.pop('MISSING', True, cast=bool))
        self.assertEqual('True', envdict.pop('MISSING', 'True', cast=bool))

    def test_update_casts(self):
        """Update the cast functions on init"""
        envdict = EnvDict({'DEBUG': '1'}, casts={'mycast': Decimal})
        self.assertEqual(envdict.get('DEBUG', cast='mycast'), Decimal('1'))

    def test_recasting(self):
        envdict = EnvDict({'DEBUG': '1'})
        self.assertEqual('1', envdict['DEBUG'])
        envdict.recast(schema={'DEBUG': int})
        self.assertEqual(1, envdict['DEBUG'])


class TestEnvInterface(unittest.TestCase):
    """
    Tests for the interface to get configuration from the local environment
    and/or a file.
    """
    def setUp(self):
        os.environ['SYSENV_TESTING_VALUE_'] = 'Okay'
        self.env_file = os.path.dirname(__file__) + '/test_env.txt'

    def test_activate_sys(self):
        """Ensure that the Env is activated using the environment"""
        env = load()
        self.assertEqual('Okay', env['SYSENV_TESTING_VALUE_'])

    def test_file_reading(self):
        self.assertEqual(22, len(read_file_values(self.env_file)))
        self.assertEqual({}, read_file_values('/thisfiledoesnotexists.txt'))
        self.assertRaises(IOError, read_file_values,
                '/thisfiledoesnotexists.txt', fail_silently=False)

    def test_load_file(self):
        env = load(self.env_file)
        self.assertTrue(env.get('SYSENV_DEBUG_VALUE_', False, cast=bool))
        self.assertFalse(env.get('BOOL_FALSE_VAR', True, cast=bool))

    def test_load_in_osenviron(self):
        """Ensure that the new values are placed into the environment"""
        load(self.env_file)
        self.assertTrue('SYSENV_DEBUG_VALUE_' in os.environ)

    def tearDown(self):
        os.environ.pop('SYSENV_TESTING_VALUE_')

if __name__ == '__main__':
    unittest.main()
