===============
Vagga To Lithos
===============

:Status: Alpha


A tool which helps to generate lithos config from a vagga config.

* vagga_ -- is a tool for development environments that runs linux containers
* lithos_ -- is a supervisor for running containers in production


.. _vagga: https://vagga.readthedocs.org
.. _lithos: https://lithos.readthedocs.org


Installation
============

Should be installable from pip::

    pip install vagga2lithos==0.1.0

But in the meantime install from github::

    pip install git+https://github.com/tailhook/vagga2lithos


Try
===

Running directly from the repo::

    vagga run generate -f examples/django/vagga.yaml run

Running installed tool (in your project directory)::

    vagga2lithos generate your-run-command


License
=======

Licensed under either of

* Apache License, Version 2.0,
  (./LICENSE-APACHE or http://www.apache.org/licenses/LICENSE-2.0)
* MIT license (./LICENSE-MIT or http://opensource.org/licenses/MIT)
  at your option.

Contribution
------------

Unless you explicitly state otherwise, any contribution intentionally
submitted for inclusion in the work by you, as defined in the Apache-2.0
license, shall be dual licensed as above, without any additional terms or
conditions.

