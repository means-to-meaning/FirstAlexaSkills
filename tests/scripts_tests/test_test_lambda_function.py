"""
Test for creating a lambda function - this has a dependency on the unpacking script as we need
the skills examples first to setup this test
"""
import os
import tempfile
import subprocess
import boto3
import time
import shutil
from FirstAlexaSkills import lambda_utils

cur_dir = os.path.dirname(os.path.realpath(__file__))
package_root_dir = os.path.dirname(os.path.dirname(cur_dir))


class TestFunctional:

    @staticmethod
    def check_lambda_reply(client, function_name, event, ref_reply):
        test_res = lambda_utils.test_lambda(client, function_name, event)
        assert test_res == ref_reply

    @classmethod
    def setup_class(cls):
        """This method does the setup and script execution once for all the tests"""
        # setup test
        # load reference reply
        cls.ref_reply = ['############################################',
                         'Testing function now!',
                         '############################################',
                         'Sending Alexa Intent: FakeIntent and slots:{}',
                         'Lambda function replied: hmm not sure how to deal with your request',
                         'Sending Alexa Intent: saySomethingIntent and slots:{}',
                         'Lambda function replied: I say whatever I please']
        # unpack the example_skills in a temp dir
        cls.output_dir = tempfile.mkdtemp()
        cls.cmd = ['unpack_example_skills', '--output-dir', cls.output_dir]
        # this will raise an exception if the return code is not 0
        std_out = subprocess.check_output(cls.cmd)
        print(std_out)
        cls.created_examples_dir = os.path.join(cls.output_dir, 'example_skills')

        # prepare running of the update script - most importantly,
        # delete any existing test functions in the cloud
        cls.alexa_event_template = lambda_utils.get_eventtemplate_fn()
        cls.alexa_test_data = os.path.join(cls.created_examples_dir, 'alexa_skill_first', 'tests',
                                           'data', 'lambda_test_data.json')
        cls.user = 'lambdaUser'
        cls.region = 'eu-west-1'
        cls.execution_role = 'basic_lambda_execute'
        cls.script = 'test_lambda_function'
        cls.skill_dir = os.path.join(cls.created_examples_dir, 'alexa_skill_first')
        cls.function_name = 'firstskill_test'
        cls.session = boto3.Session(profile_name=cls.user, region_name=cls.region)
        cls.client = cls.session.client('lambda')
        # check if lambda function exists and if yes, delete it
        existing_funs_list = lambda_utils.list_lambda_functions(cls.client)
        if cls.function_name in existing_funs_list:
            response = cls.client.delete_function(FunctionName=cls.function_name)
            print(response)
        create_cmd = ['create_lambda_function', '--function-name', cls.function_name, '--dir',
                      cls.skill_dir, '--execution-role', cls.execution_role]
        cls.cmd = [cls.script, '--function-name', cls.function_name, '--dir',  cls.skill_dir,
                   '--execution-role', cls.execution_role, '--test-data', cls.alexa_test_data]
        time.sleep(1)
        existing_funs_list = lambda_utils.list_lambda_functions(cls.client)
        if cls.function_name in existing_funs_list:
            raise Exception("Lambda function already exists - "
                            "perhaps it couldn't be deleted correctly?!")
        else:
            # this will raise an exception if the return code is not 0
            std_out = subprocess.check_output(create_cmd)
            print(std_out)
            existing_funs_list = lambda_utils.list_lambda_functions(cls.client)
            if cls.function_name not in existing_funs_list:
                raise Exception("Lambda function couldn't be created - "
                                "test setup failed")

    @classmethod
    def teardown_class(cls):
        """This method is run once for each class _after_ all tests are run"""
        # delete the created function
        if os.path.exists(cls.output_dir):
            shutil.rmtree(cls.output_dir)
        # delete the created function
        existing_funs_list = lambda_utils.list_lambda_functions(cls.client)
        if cls.function_name in existing_funs_list:
            response = cls.client.delete_function(FunctionName=cls.function_name)
            print(response)

    def test_function_works(self):
        try:
            proc = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            std_out, std_err = proc.communicate()
            std_out_str_list = str(std_out.decode()).splitlines()
            std_out_str_list = [l.strip() for l in std_out_str_list]
            std_out_str_list = std_out_str_list[:7]
            std_err_str = str(std_err.decode())
            is_stdout_asexpected = (set(std_out_str_list) == set(self.ref_reply))
            is_stderr_asexpected = (std_err_str == '')
            assert is_stdout_asexpected and is_stderr_asexpected and proc.returncode == 0
        except Exception:
            assert False
