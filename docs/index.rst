.. FirstAlexaSkills documentation master file, created by
   sphinx-quickstart on Tue Mar 14 21:58:22 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to FirstAlexaSkills
===========================

``FirstAlexaSkills`` is a Python package with example Alexa skills and utilities
that will enable you to quickly and confidently develop third party Alexa Skills
using AWS Lambda. The tutorials will guide you in developing skills with increasing
complexity, starting from basics and using test-driven development to add additional
layers of functionality.

Installation
------------
You can install ``FirstAlexaSkills`` with ``pip``:

.. code-block:: console

    $ pip install firstalexaskills

See :doc:`Installation <installation>` for more information.

Why a package for making Alexa Skills?
--------------------------------------

If you haven't developed Alexa skills before, the workflow can seem overwhelming.
If you have developed skills before, you will agree that having a workflow for
developing and testing the Lambda code really makes the difference between
happiness and despair. This package addresses:

* Automated testing for Lambdas
* User-friendly generation of fake Alexa events
* Minimizes manual AWS console interactions
* Examples with progressive skill difficulty - from simple to complex
* Beginner friendly commandline tools - perfect for a Hackathon

Layout
------

``FirstAlexaSkills`` consists of three bits: the example_skills, commandline tools that suppport your development and tutorials that you can follow.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   tutorials
   hackathon_setup
   python_intro
   FirstAlexaSkills
   develop.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
