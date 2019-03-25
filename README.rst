**Yet Another Form WIdget Library**.

.. image:: https://img.shields.io/pypi/v/yafowil.svg
    :target: https://pypi.python.org/pypi/yafowil
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/yafowil.svg
    :target: https://pypi.python.org/pypi/yafowil
    :alt: Number of PyPI downloads


YAFOWIL offers html-form creation and modification at runtime. 
It is light-weight and provides an extensible, reusable set of blueprints to build flexible forms.

YAFOWIL is independent from any web-framework, but easy to use in your web-framework.

It's all just about rendering widgets and extracting the data returned from the browser per widget. 
It does not fight with storage.

YAFOWIL vary from most other HTML form packages: Its all just configuration. 
No subclassing needed any more; no specific schema-framework is necessary.

Yafowil provides a factory where you can fetch your widgets instances from.
Or you register your own.


Detailed Documentation
======================

If you're interested to dig deeper: i
The `detailed YAFOWIL documentation <http://docs.yafowil.info>`_ is available. 
Read it and learn how to create your example application with YAFOWIL forms in 15 minutes.


Source Code
===========

.. image:: https://travis-ci.org/bluedynamics/yafowil.svg?branch=master
    :target: https://travis-ci.org/bluedynamics/yafowil

The sources are in a GIT DVCS with its main branches at
`github <http://github.com/bluedynamics/yafowil>`_.

We'd be happy to see many forks and pull-requests to make YAFOWIL even better.

Coverage report::

    Name                           Stmts   Miss  Cover
    --------------------------------------------------
    src/yafowil/__init__.py            0      0   100%
    src/yafowil/base.py              363      0   100%
    src/yafowil/common.py            884      1    99%
    src/yafowil/compat.py              8      0   100%
    src/yafowil/compound.py          100      1    99%
    src/yafowil/controller.py         44      0   100%
    src/yafowil/example.py            58      0   100%
    src/yafowil/i18n/__init__.py       0      0   100%
    src/yafowil/loader.py              9      0   100%
    src/yafowil/persistence.py        10      0   100%
    src/yafowil/resources.py          33      0   100%
    src/yafowil/table.py              51      0   100%
    src/yafowil/tsf.py                19      0   100%
    src/yafowil/utils.py             214      5    98%
    --------------------------------------------------
    TOTAL                           1793      7    99%


Contributors
============

- Jens W. Klein

- Robert Niederreiter

- Johannes Raggam

- Peter Holzer

- Attila Olah

- Florian Friesdorf

- Daniel Widerin

- Georg Bernhard

- Christian Scholz aka MrTopf
