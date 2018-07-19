#!/usr/bin/env python

import os
import sys
import logging
import shutil
import json
import copy
import collections
import tempfile
import time
import boto3
import pkg_resources

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - '
                           '%(message)s', datefmt='%Y/%m/%d %I:%M:%S %p',
                    level=logging.ERROR)

cur_dir = os.path.dirname(os.path.realpath(__file__))


def get_skills_archive_fn():
    resource_package = "FirstAlexaSkills"
    # Do not use os.path.join()!
    resource_path = '/'.join(('data', 'example_skills.zip'))
    my_filename = pkg_resources.resource_filename(resource_package,
                                                  resource_path)
    return my_filename


def get_eventtemplate_fn():
    resource_package = "FirstAlexaSkills"
    # Do not use os.path.join()!
    resource_path = '/'.join(('data', 'event_template.json'))
    my_filename = pkg_resources.resource_filename(resource_package,
                                                  resource_path)
    return my_filename


def get_account_id(profile_name, region=None):
    owner_id = None
    session = boto3.Session(profile_name=profile_name, region_name=region)
    client = session.client('ec2')
    response = client.describe_security_groups()
    if 'SecurityGroups' in response:
        owner_id = response['SecurityGroups'][0]['OwnerId']
    return owner_id


def get_execrole_arn(execrole_name, profile_name, region=None):
    account_id = get_account_id(profile_name, region)
    execrole_arn = 'arn:aws:iam::' + account_id + ':role/' + execrole_name
    return execrole_arn


def list_lambda_functions(client):
    function_name_list = []
    # Create a reusable Paginator
    paginator = client.get_paginator('list_functions')
    # Create a PageIterator from the Paginator
    page_iterator = paginator.paginate()
    for page in page_iterator:
        for function in page['Functions']:
            function_name_list.append(function['FunctionName'])
    return function_name_list


def create_zipfile(dir_path):
    zip_dir = tempfile.mkdtemp()
    ext = 'zip'
    function_zip = "function"  # will produce a zip archive
    shutil.make_archive(os.path.join(zip_dir, function_zip), ext, dir_path)
    return os.path.join(zip_dir, function_zip + '.' + ext)


def create_lambda(client, function_name, dir_path, role):
    # Todo: infer environment from file suffix
    # Todo: add support for packing virtualenv for Python
    logger = logging.getLogger(__name__)
    zip_file = ""
    fun_arn = None
    try:
        runtime = 'python3.6'
        zip_file = create_zipfile(dir_path)
        response = client.create_function(
            FunctionName=function_name,
            Runtime=runtime,
            Role=role,
            Handler='lambda_function.lambda_handler',
            Code={
                'ZipFile': open(zip_file, 'rb').read()
            },
            Description='autmatically uploaded',
            Timeout=5,
            MemorySize=128,
            Publish=True
        )
        http_resp = response["ResponseMetadata"]["HTTPStatusCode"]
        if http_resp == 201 and"FunctionArn" in response:
            fun_arn = response["FunctionArn"]
        logger.debug(response)
        response = client.add_permission(
            FunctionName=function_name,
            StatementId='1',
            Action='lambda:invokeFunction',
            Principal='alexa-appkit.amazon.com'
        )
        logger.debug(response)
    # print(response)
    except Exception as e:
        print(str(e))
    finally:
        # remove the temp dir containing the zipfile
        if os.path.exists(zip_file):
            shutil.rmtree(os.path.dirname(zip_file))
    return fun_arn


def update_lambda(client, function_name, dir_path):
    logger = logging.getLogger(__name__)
    zip_file = ""
    try:
        zip_file = create_zipfile(dir_path)
        zip_file_handle = open(zip_file, 'rb')
        response = client.update_function_code(
            FunctionName=function_name,
            ZipFile=zip_file_handle.read(),
            Publish=True
        )
        logger.debug(response)
    except Exception as e:
        print(str(e))
    finally:
        # remove the temp dir containing the zipfile
        if os.path.exists(zip_file):
            shutil.rmtree(os.path.dirname(zip_file))


def replace_nested_dict_val(orig_dict, k, v):
    for key, val in list(orig_dict.items()):
        if key == k:
            orig_dict[key] = v
        elif isinstance(val, collections.Mapping):
            replace_nested_dict_val(orig_dict.get(key, {}), k, v)
    return orig_dict


def generate_testevents(test_data, event_template):
    event_list = []
    with open(test_data) as f:
        tests_list = json.load(f)
    with open(event_template) as f:
        template = json.load(f)
    for test in tests_list:
        new_event = copy.deepcopy(template)
        for k, v in list(test.items()):
            new_event = replace_nested_dict_val(new_event, k, v)
        event_list.append(copy.deepcopy(new_event))
    return event_list


def run_all_tests(client, function_name, alexa_event_data, event_template):
    event_list = generate_testevents(alexa_event_data, event_template)
    for event in event_list:
        reply_text = test_lambda(client, function_name, event)
        if reply_text:
            print("Lambda function replied: " + str(reply_text))
        else:
            print("Lambda function didn't reply!!!")
        time.sleep(1)


def test_lambda(client, function_name, event):
        reply_text = None
        print("Sending Alexa Intent: " + event["request"]["intent"]["name"] +
              " and slots:" + str(event["request"]["intent"]["slots"]))
        event_binary = bytearray()
        event_binary.extend(json.dumps(event).encode())
        response = client.invoke(
            FunctionName=function_name,
            InvocationType='RequestResponse',
            LogType='Tail',
            Payload=event_binary
        )
        try:
            res = response["Payload"].read()
            reply_json = json.loads(res)
            reply_text = reply_json["response"]["outputSpeech"]["text"]
        except Exception:
            print("Lambda function returned an error:")
            print_nested(reply_json)
        return reply_text


def print_nested(obj, nested_level=0, output=sys.stdout):
    spacing = '   '
    if type(obj) == dict:
        # print >> output, '%s{' % ((nested_level) * spacing)
        for k, v in list(obj.items()):
            if hasattr(v, '__iter__'):
                print('%s%s:' % ((nested_level + 1) * spacing, k))
                print_nested(v, nested_level + 1, output)
            else:
                print('%s%s: %s' % ((nested_level + 1) * spacing, k, v))
        # print >> output, '%s}' % (nested_level * spacing)
    elif type(obj) == list:
        print('%s' % ((nested_level) * spacing))
        for v in obj:
            if hasattr(v, '__iter__'):
                print_nested(v, nested_level + 1, output)
            else:
                print('%s%s' % ((nested_level + 1) * spacing, v))
        # print >> output, '%s' % ((nested_level) * spacing)
    else:
        print('%s%s' % (nested_level * spacing, obj))
