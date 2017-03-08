"""
Test for updating a lambda function - this has a dependency on the
unpacking script as we need the skills examples first to setup this
test and on the creating script as the function must exist
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


class TestFunctional():

    @staticmethod
    def check_lambda_reply(client, function_name, event, ref_reply):
        test_res = lambda_utils.test_lambda(client, function_name, event)
        assert test_res == ref_reply

    @classmethod
    def setup_class(cls):
        """
        This method does the setup and script execution once for all the tests
        """
        # setup test
        # unpack the example_skills in a temp dir
        cls.output_dir = tempfile.mkdtemp()
        cls.cmd = ['unpack_example_skills', '--output-dir', cls.output_dir]
        # this will raise an exception if the return code is not 0
        # TODO: log process output
        # this will raise an exception if the return code is not 0
        std_out = subprocess.check_output(cls.cmd)
        print(std_out)
        cls.created_examples_dir = os.path.join(cls.output_dir, 'example_skills')

        # prepare running of the update script - most importantly delete
        # any existing test functions in the cloud
        cls.alexa_event_template = lambda_utils.get_eventtemplate_fn()
        cls.alexa_test_data = os.path.join(cls.created_examples_dir, 'alexa_skill_saysomething',
                                           'lambda_test_data.json')
        cls.user = 'testFirstAlexaSkilluser'
        cls.region = 'eu-west-1'
        account_id = lambda_utils.get_account_id(profile_name=cls.user, region=cls.region)
        cls.execution_role = 'arn:aws:iam::' + account_id + ':role/basic_lambda_execute'
        cls.script = 'update_lambda_function'
        cls.skill_dir = os.path.join(cls.created_examples_dir, 'alexa_skill_saysomething')
        cls.function_name = 'saysomething_test'
        cls.session = boto3.Session(profile_name=cls.user,
                                    region_name=cls.region)
        cls.client = cls.session.client('lambda')
        # check if lambda function exists and if yes, delete it
        existing_funs_list = lambda_utils.list_lambda_functions(cls.client)
        if cls.function_name in existing_funs_list:
            response = cls.client.delete_function(FunctionName=cls.function_name)
            print(response)
        cls.cmd = [cls.script, '--function-name', cls.function_name,
                   '--dir',  cls.skill_dir,
                   '--test-data', cls.alexa_test_data]
        existing_funs_list = lambda_utils.list_lambda_functions(cls.client)
        if cls.function_name in existing_funs_list:
            raise Exception("Lambda function already exists - "
                            "perhaps it couldn't be deleted correctly?!")
        time.sleep(1)
        # create the function so that we can update it
        create_cmd = ['create_lambda_function', '--function-name', cls.function_name,
                      '--dir', cls.skill_dir, '--execution-role', cls.execution_role,
                      '--test-data', cls.alexa_test_data]
        subprocess.call(create_cmd)

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
            std_err_str = str(std_err.decode())
            print(std_out_str_list)
            print(std_err_str)
            # TODO: log output
            assert proc.returncode == 0
        except Exception:
            assert False
