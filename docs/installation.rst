============
Installation
============

1. Install the ``FirstAlexaSkills`` package and its dependencies

   .. code-block:: console

        $ pip install firstalexaskills

2. Create an Amazon `developer account`_
3. Create an `AWS account`_ (`the first million AWS Lambda calls are free`_)
4. Create an `IAM user`_ called 'lambdaUser' for running and updating the AWS Lambda functions. The user will require the 'AWSLambdaFullAccess' permissions. Make sure to check "Programmatic access" when creating the user. The AWS website will generate an `access key`_ for you, which you can download in .csv file. We will use the credentials in the next step.
5. Configure the AWS CLI to use credentials of your new IAM user

   .. code-block:: console

        $ aws configure --profile lambdaUser

   Paste the information from credentials.csv into your `command line`_:

   * Access key ID
   * Secret access key
   * an aws region of your choice - example: eu-west-1
   * format: json


6. Create an `execution role for AWS Lambda`_ functions.

   Preferably use 'basic_lambda_execute' as name for the role, since the package uses it as default. Unless you expect your function to require special privileges, like access to S3, use the official policy 'AWSLambdaExecute'.

7. Verify that the IAM user is setup correctly:

   .. code-block:: console

        $ aws lambda list-functions --profile lambdaUser
        {
            "Functions": []
        }

.. _`command line`: http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html
.. _`developer account`: https://developer.amazon.com/
.. _`AWS account`: https://aws.amazon.com/
.. _`the first million AWS Lambda calls are free`: https://aws.amazon.com/lambda/pricing/
.. _`IAM user`: http://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html
.. _`execution role for AWS Lambda`: http://docs.aws.amazon.com/lambda/latest/dg/with-s3-example-create-iam-role.html
.. _`access key`: http://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#access-keys-and-secret-access-keys