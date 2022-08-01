User guide
==========

Requirements
------------

- Python 3.6+
- Hamlib 3.3+ Python bindings


Installation
------------

Debian
^^^^^^

To install the required dependencies in Debian run::

  $ apt-get install python3-libhamlib2


SatNOGS Client
^^^^^^^^^^^^^^

To install SatNOGS Client run::

  $ pip install satnogs-client

This will install a console script called ``satnogs-client``.


.. _configuration:

Configuration
-------------

Configuration of SatNOGS Client is done through environment variables.
The environment variables can also be defined in a file called ``.env``, place on the project root directory.
The format of each line in ``.env`` file is ``VARIABLE=VALUE``.

.. include:: environment_variables.rst


Usage
-----

To execute the script, run it on the command line::

  $ satnogs-client
