Develop
=======

.. role:: con(code)
   :language: console

This assumes that you went through the installation and setup notes. To develop the example skills and this package will require working AWS credentials.

.. caution:: Some of the tests in this project require AWS credentials as they perform end-to-end testing including cloud upload. Specifically tests in tests/scripts (test the commandline tools) tests/functional (end-to-end tests of skills functionality). During development, tests should only be run using :con:`$ python setup.py test -a '-e cloud'`. Travis CI will only runs local tests using :con:`$ python setup.py test`. That means that Travis does not guarantee that your commit won't break the build and the resposnsibility for cloud tests lies with you!!

Here are a few steps to get you started:

.. code-block:: console

 $ git clone https://github.com/means-to-meaning/FirstAlexaSkills
 $ mkvirtualenv python27fasdev --no-site-packages
 $ activate python27fas
 $ cd FirstAlexaSkills
 $ python setup.py develop # or pip install -e .
 __________ do some work __________
 $ python setup.py test -a '-e cloud' # this will run all the tests including end-end cloud stuff
 $ restview docs/develop.rst # view docs in browser while modifying them
 $ sphinx-apidoc -F -o docs FirstAlexaSkills # generate sphinx autodoc documentation
 $ python setup.py develop --uninstall # or pip uninstall FirstAlexaSkills
 $ python setup.py test
 $ deactivate