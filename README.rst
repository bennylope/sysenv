=======================================
SysEnv: the environment variable helper
=======================================

.. image:: https://badge.fury.io/py/sysenv.png
    :target: http://badge.fury.io/py/sysenv

.. image:: https://travis-ci.org/bennylope/sysenv.png?branch=master
        :target: https://travis-ci.org/bennylope/sysenv

.. image:: https://pypip.in/d/sysenv/badge.png
        :target: https://crate.io/packages/sysenv?version=latest

Simple handling of system environment variables for application deployment.

SysEnv lets you configure your Python application using environment variables,
casting types as necessary, enabling smooth `12factor deployments <http://12factor.net/>`_.

It's a replacement for `an inline function
<http://wellfireinteractive.com/blog/easier-12-factor-django/>`_, with some
inspiration and code from `Honcho <https://github.com/nickstenning/honcho>`_.
The interface is directly inspired by `Django-environ
<https://github.com/joke2k/django-environ>`_ but unlike Django-environ SysEnv
is not Django specific and does not replace functionality provided by existing
applications.

* Free software: BSD license
* Documentation: http://sysenv.rtfd.org.

Installation
============

    pip install sysenv

Using SysEnv
============

To load from your local environment, use the `load` function to return an
`EnvDict` instance.::

    >>> from sysenv import load
    >>> env = load()

By default it loads from the system environment, but you can also include
values from a `.env` or similar file.::

    >>> from sysenv import load
    >>> env = load('.env')

The `EnvDict` instance can be accessed like a normal Python dictionary.::

    >>> env['DEBUG']
    'True'
    >>> env.get('DEBUG', False)
    'True'

Of course your environment variables are strings, so you'll want to cast the
return value to a boolean.::

    >>> env.get('DEBUG', False, cast=bool)
    True

Alternatively you can define a schema when you initialize your `EnvDict`.::

    >>> env = EnvDict(schema={'DEBUG': bool, 'CACHE_COUNT': int})
    >>> env = load(schema={'DEBUG': bool, 'CACHE_COUNT': int})

The schema should be provided as a dictionary of key names with the cast
identifier given as the value in the schema.

Using with Django
-----------------

To use SysEnv in your Django project add it to the top of your settings.py file
and pull in setting values from the `env` variable (or whatever you call it).::

    from sysenv import load
    env = load('.env')
    DEBUG = env.get('DEBUG', False, cast=bool)

See the `docs <http://sysenv.readthedocs.org/en/latest/>`_ for
additional usage instructions.
