"""
Test comparing the folder created by unpack_example_skills script
from the package (using package_data) with the example_skills folder in the repo -
this can and should only be run in development mode
since we are testing repo file structure against package data
"""
import os
import tempfile
import subprocess
import shutil

cur_dir = os.path.dirname(os.path.realpath(__file__))


class TestFunctional():

    @classmethod
    def setup_class(cls):
        """This method does the setup and script execution once for all the tests"""
        # setup test
        cls.script = 'unpack_example_skills'
        cls.output_dir = tempfile.mkdtemp()
        cls.created_examples_dir = os.path.join(cls.output_dir, 'example_skills')
        cls.cmd = [cls.script, '--output-dir', cls.output_dir]

    @classmethod
    def teardown_class(cls):
        """This method is run once for each class _after_ all tests are run"""
        # delete the created function
        if os.path.exists(cls.output_dir):
            shutil.rmtree(cls.output_dir)

    def test_function_works(self):
        try:
            proc = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            std_out, std_err = proc.communicate()
            assert proc.returncode == 0 and os.path.exists(self.created_examples_dir)
        except Exception:
            assert False
