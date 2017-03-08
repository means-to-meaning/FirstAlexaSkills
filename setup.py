"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
import os
from os import path
import sys
from setuptools.command.test import test as TestCommand

base_dir = os.path.dirname(__file__)
src_dir = os.path.join(base_dir, "src")

# Get the long description from the README file
with open(path.join(base_dir, 'README.rst')) as f:
    long_description = f.read()


class Tox(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import tox
        errcode = tox.cmdline(self.test_args)
        sys.exit(errcode)


setup(
    name='FirstAlexaSkills',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.1.0',

    description='A package for learning first steps with Alexa skills',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/means-to-meaning/FirstAlexaSkills',

    # Author details
    author='Vlastimil Pis',
    author_email='vlasto.pis@gmail.com',

    # Choose your license
    license='Amazon Software license',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Education',
        'Topic :: Home Automation',

        # Pick your license as you wish (should match "license" above)
        'License :: Other/Proprietary License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ],

    # What does your project relate to?
    keywords='alexa skills echo iot aws lambda',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    # include_package_data=True,

    # this does not work in development mode!!!
    # packages=['FirstAlexaSkills'],
    # package_dir={'FirstAlexaSkills': 'src/FirstAlexaSkills'},


    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['awscli', 'boto3', 'AWSIoTPythonSDK'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    tests_require=['tox'],
    cmdclass={'test': Tox},

    extras_require={
        # 'dev': ['check-manifest'],
        # 'test': ['nose', 'coverage'],
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={'FirstAlexaSkills': ['data/event_template.json',
                                         'data/example_skills.zip']},

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('data', ['data/data_file'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    # entry_points={
    #     'console_scripts': [
    #         'sample=sample:main',
    #     ],
    # },
    scripts=['bin/unpack_example_skills',
             'bin/update_lambda_function',
             'bin/create_lambda_function']
)
