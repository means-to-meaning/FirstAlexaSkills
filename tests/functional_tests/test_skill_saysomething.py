
import os
import time
import boto3
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
        # setup test:
        cls.user = 'testFirstAlexaSkilluser'
        cls.region = 'eu-west-1'
        account_id = lambda_utils.get_account_id(profile_name=cls.user, region=cls.region)
        cls.execution_role = 'arn:aws:iam::' + account_id + ':role/basic_lambda_execute'
        cls.dir = os.path.join(package_root_dir, 'example_skills', 'alexa_skill_saysomething')
        cls.event_template = os.path.join(package_root_dir, 'src', 'FirstAlexaSkills', 'data',
                                          'event_template.json')
        cls.alexa_event_data = os.path.join(package_root_dir, 'example_skills',
                                            'alexa_skill_saysomething', 'lambda_test_data.json')
        # not generating random names on purpose,
        # if things go wrong, we don't pollute the account
        cls.function_name = 'saysomething_test'
        cls.session = boto3.Session(profile_name=cls.user, region_name=cls.region)
        cls.client = cls.session.client('lambda')
        # create the function if it doesn't exist
        existing_funs_list = lambda_utils.list_lambda_functions(cls.client)
        if cls.function_name in existing_funs_list:
            response = cls.client.delete_function(FunctionName=cls.function_name)
            print(response)
            time.sleep(1)
        fun_arn = lambda_utils.create_lambda(cls.client, cls.function_name, cls.dir,
                                             cls.execution_role)
        if fun_arn:
            print("Function succesfully created!")
            print("AWS Lambda function ARN: " + str(fun_arn))
        else:
            raise Exception("Failed to create Lambda function when setting up test!")
        cls.event_list = lambda_utils.generate_testevents(cls.alexa_event_data, cls.event_template)
        cls.ref_reply_list = [None,
                              "I say whatever I please",
                              "I say whatever I please"]

    @classmethod
    def teardown_class(cls):
        """This method is run once for each class _after_ all tests are run"""
        # delete the created function
        session = boto3.Session(profile_name=cls.user, region_name=cls.region)
        client = session.client('lambda')
        # create the function if it doesn't exist
        existing_funs_list = lambda_utils.list_lambda_functions(client)
        if cls.function_name in existing_funs_list:
            response = client.delete_function(FunctionName=cls.function_name)
            print(response)

    def test_function_works(self):
        for i in range(len(self.event_list)):
            event = self.event_list[i]
            ref_reply = self.ref_reply_list[i]
            fname = self.function_name
            yield TestFunctional.check_lambda_reply, self.client, fname, event, ref_reply,
