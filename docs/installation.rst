Installation
============

1. Install the ``FirstAlexaSkills`` package and its dependencies

    .. code-block:: console

        $ pip install FirstAlexaSkills

2. Create an Amazon `developer account`_
3. Create an `AWS account`_ (`the first million AWS Lambda calls are free`_)
4. Create an `IAM user`_ called 'lambdaUser' for running and updating the AWS Lambda functions. The user will require the 'AWSLambdaFullAccess' permissions.
5. Configure the AWS CLI to use credentials of your new IAM user

    .. code-block:: console

        $ aws configure --profile lambdaUser --region eu-west-1

6. Create an `execution role for AWS Lambda`_ functions

 Preferably use 'basic_lambda_execute' as name for the role, since the package uses it as default. Unless you expect your function to require special privileges, like access to S3, use the official policy 'AWSLambdaExecute'.

.. _`developer account`: https://developer.amazon.com/
.. _`AWS account`: https://aws.amazon.com/
.. _`the first million AWS Lambda calls are free`: https://aws.amazon.com/lambda/pricing/
.. _`IAM user`: http://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html
.. _`execution role for AWS Lambda`: http://docs.aws.amazon.com/lambda/latest/dg/with-s3-example-create-iam-role.html