Developer guide
===============

Installation
------------

To install the required dependencies in Debian Bullseye run::

  $ apt-get install libatlas3-base libhdf5-103-1 python3-gps python3-libhamlib


It is recommended to install the client in a virtualenv.
The virtualenv needs to have access to system Python bindings.
To create the virtualenv, you can use ``virtualenvwrapper``.
On the first time, create the virtualenv by running::

  $ mkvirtualenv --system-site-packages -a . satnogs-client

To activate the virtualenv after it is created run::

  $ workon satnogs-client

To install SatNOGS Client for development run in the project root directory::

  $ pip install -e .[dev]


Configuration
-------------

This project uses ``python-dotenv``.
Configuration of ``satnogsclient/settings.py`` can be overridden by setting the respective environment variables or an ``.env`` file placed on the project root directory.
Check :ref:`configuration` for a list of all configuration variables.

Code Quality Assurance
----------------------

The following code quality assurance tools are used in this project:

  * ``flake8``
  * ``isort``
  * ``yapf``
  * ``pylint``
  * ``robotframework``

Testing
-------

System testing
^^^^^^^^^^^^^^

Robot Framework is used for system testing.
``robot/testsuites`` contain Robot test cases and suites.


Automation
----------

``tox`` is used to automate development tasks.
To execute the default list of tasks run::

  $ tox


Environments
^^^^^^^^^^^^

The following ``tox`` environments are available:

  * ``flake8`` - Check code for common errors, coding style and complexity
  * ``isort`` - Check code for correct imports order
  * ``isort-apply`` - Sort imports
  * ``yapf`` - Check code for correct formatting
  * ``yapf-apply`` - Reformat source code
  * ``pylint`` - Execute static code analysis
  * ``build`` - Build source and binary distributions
  * ``upload`` - Upload source and binary distributions to PyPI
  * ``docs`` - Build documentation
  * ``robot-lint`` - Lint system test cases and suites
  * ``robot-tidy`` - Reformat system test cases and suites
  * ``robot`` - Execute system testing

To execute a single environment run::

  $ tox -e <environment>
