=====
Usage
=====

To load from your local environment, use the `load` function to return an
`EnvDict` instance.::

    >>> from sysenv import load
    >>> env = load()

By default it loads from the system environment, but you can also include
values from a `.env` or similar file.::

    >>> from sysenv import load
    >>> env = load('.env')

.. note::

    The load function returns a new `EnvDict` instance and also updates the
    system environment with values in the provided file so that later calles to
    `os.environ` will pick up on these new variables or values.

The `EnvDict` instance can be accessed like a normal Python dictionary.::

    >>> env['DEBUG']
    'True'
    >>> env.get('DEBUG', False)
    'True'

Of course your environment variables are strings, so you'll want to cast the
return value to a boolean.::

    >>> env.get('DEBUG', False, cast=bool)
    True

Type schemas
============

Alternatively you can define a schema when you initialize your `EnvDict`. For
example, to ensure that the value for `DEBUG` is rendered internally as a
boolean value and `CACHE_COUNT` is rendred as an integer::

    >>> env = EnvDict(schema={'DEBUG': bool, 'CACHE_COUNT': int})
    >>> env.get('DEBUG')
    True
    >>> env['DEBUG']
    True
    >>> env = load(schema={'DEBUG': bool, 'CACHE_COUNT': int})
    >>> env.get('CACHE_COUNT')
    3600
    >>> env['CACHE_COUNT']
    3600

The schema should be provided as a dictionary of key names with the cast
identifier given as the value in the schema.

Type casting
============

By default an EnvDict instance can cast to these types:

    * `str` (default)
    * `bool`
    * `int`
    * `float`
    * `Decimal`
    * `list`
    * `dict`

Each type can be cast using a built-in dictionary that uses the type (by type
object or name) as the key and the type constructor or other passable function
as the value.

All built-in types are cast using the type as the casting dictionary key, e.g.::

    env.get('MY_VAR', cast=list)

Non-built in types should be referenced by lowercased string name, e.g.::

    env.get('MY_VAR', cast='decimal')

bool conversion
---------------

Booleans are cast by comparing the lowercased input against a tuple of "true"
values:

    * true
    * on
    * yes
    * 1

`True` is returned if the filtered input is in the tuple, otherwise `False`.

list converstion
----------------

The list conversion produces a list of strings based on the input, e.g. it will
turn::

    MYVAR=1,2,3,4

Into::

    >>> env.get('MYVAR', cast=list)
    ['1', '2', '3', '4']

dictionary conversion
---------------------

The dictionary conversion produces a dictionary of string keys and values based
on the input, e.g. it will turn::

    MYVAR=a=1,b=2,c=3,d=4

Into::

    >>> env.get('MYVAR', cast=dict)
    {'a': '1', 'b': '2', 'c': '3', 'd': '4'}

Extending type casting
----------------------

You can replace or add type casting methods. Simply pass a dictionary using the
`casts` keyword when creating an `EnvDict` instance.::

    >>> MY_TRUE_VALUES = ('true', 'for sure')
    >>> env = EnvDict({'DEBUG': 'For SURE'}, casts={bool: lambda x: x.lower in MY_TRUE_VALUES})
    >>> env.get('DEBUG', cast=bool)
    True

The same dictionary can be based when loading the environment.::

    >>> MY_TRUE_VALUES = ('true', 'for sure')
    >>> env = load(casts={bool: lambda x: x.lower in MY_TRUE_VALUES})
    >>> env.get('DEBUG', cast=bool)
    True

Using with Django
=================

To use SysEnv in your Django project add it to the top of your settings.py file
and pull in setting values from the `env` variable (or whatever you call it).::

    from sysenv import load
    env = load('.env')
    DEBUG = env.get('DEBUG', False, cast=bool)

Note that SysEnv does not offer functionality for configuring database or
working with file paths. There are already libraries that do those things.

You can configure your database(s) using `DJ-Database-URL
<https://github.com/kennethreitz/dj-database-url>`_.::

    DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}

Got search? You can use `DJ-Search-URL
<https://github.com/dstufft/dj-search-url>`_.::

    HAYSTACK_CONNECTIONS = {"default": dj_search_url.conf("elasticsearch://..")}

If you want to make working with file paths simpler you should take a look at
`path.py <https://pypi.python.org/pypi/path.py>`_.
