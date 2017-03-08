FirstAlexaSkills - A Python package for learning first steps with Alexa skills
==============================================================================

Welcome to the wonderful world of Alexa interactions! Do you have great ideas for teaching Alexa new skills? There are only two steps to make a third-party skill using the `Alexa Skills Kit`_:

* creating an Alexa skill (ASK) which will convert your speech into intents (think of them as events for now) which you define - by associating utterances (sentences) to intents. For more details, take a look at the `official ASK starter guide`_.
* creating an `AWS Lambda`_ function or a web service that will receive the intents from Alexa. This package uses AWS Lambda functions because they are ideal for simple functions - `low cost`_ and zero infrastructure maintainance. You can find the official documentation `here`_. If you are interested in a web service approach to ASK with Python, then you should definitely try John Wheeler's great `flask-ask package`_.


Three example skills and a tutorial guiding you from simply getting the Echo to reply, to setting your home temperature using the IoT device of your choice. Most importantly though, it allows you to develop locally, sync your local Lambda function to the cloud and immediately test it using a fake Alexa event in one button press. Something that might come in handy when building your own skills later.

The proposed development workflow is:

.. code-block:: console

    $ mkdir alexa_development
    $ unpack_example_skills # Start with a working template for an AWS Lambda function
    $ cd example_skills # Explore the Alexa skills in this directory and then create your first function
    $ create_lambda_function --function-name saysomething --dir alexa_skill_saysomething --execution-role $EXECUTION_ROLE --test-data alexa_skill_saysomething/lambda_test_data.json
    $ <YOUR_FAV_EDITOR_HERE> alexa_skill_saysomething/lambda_function.py # modify the skill to reply something different
    $ update_lambda_function # update the function in the cloud and test it

Setup and requirements
----------------------

1. Install the ``FirstAlexaSkills`` package and its dependencies

     .. code-block:: console

        $ pip install FirstAlexaSkills

2. Create an Amazon `developer account`_
3. Create an `AWS account`_ (`the first million AWS Lambda calls are free`_)
4. Create an IAM user called 'lambdaUser' for running and updating the AWS Lambda functions
    (TODO: add the right policy for the user)
5. Configure the AWS CLI to use credentials of your new IAM user

     .. code-block:: console

        $ aws configure --profile lambdaUser --region us-east1

6. create an execution role for AWS Lambda functions
    TODO: add link

Tutorial on creating Alexa third-party skills
---------------------------------------------

Say something! (alexa_skill_saysomething)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Challenge:**
Create an Alexa third-party skill that you can tell a phrase: "Alexa, ask <my_skill_name> to say something!" and it replies: "I can say whatever you want me to say".

**Suggested steps:**

1. Pick a name for your AWS Lambda function
2. Run update_lambda_function (TODO: add example params)
3. Have a look at our example: data/example_skills/alexa_skill_saysomething/lambda_function.py
4. Try to follow the execution flow which starts in the function lambda_handler()
5. By now you you should be completely confused and frustrated from staring at incomprehensible code logic dealing with some uknown objects called event and intent. So here is what is going on: Imaging you tell the Echo something like 'Alexa, ask magic skill to say something'. Your Alexa skill (which isn't created yet but will be in a few steps) will be used to convert the words 'say something' to an 'intent'. Alexa will then send this 'intent' to your AWS Lambda function which will process it, and send a reply within seconds back to Alexa. Ok, this is still a lot to process. It's enough for now if you understand two things: A. In your Alexa skill, you will define which sentences (utterances) correspond to which intents. B. When you speak to an Echo, the AWS Lambda function (the Python code you've been looking at) will receive an intent and will process it.
6. If at this point, it might be useful to have a look at an example Alexa 'event' object: data/test_event_template.json this is what the function
7. Go through the execution flow of our lambda_function.py again, but this time pay special attention to the function on_intent() function


What's cool? (alexa_skill_whatscool)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Challenge:**
Teach Alexa about what is cool. Currently the example skill chooses randomly between three replies what is the coolest movie ever. Can you teach it what are some other cool things? (bands?  food?)

**Suggested steps:**


Light on! (alexa_iot_skill)
~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Challenge:**
Communicate with any Internet capable (IoT) device in your home through Alexa securely (no open ports in your firewall required), instantaneously (1-3 seconds to reach your device) and cheaply (both in terms of $$$ and kW/h). This can include anything from an Arduino to your PC.

**Overview**:

The goal of this example is to automate as much as possible behind the scenes and allow you to focus on your IoT logic, that means handling of the intents on the device and formulation of the replies. We will use MQTT for communicating messages between our AWS Lambda function and our device, use AWS IoT to keep track of devices and get access to a ton of additional funcitonality (like rules and notifications). We have selected a Raspberry Pi as our IoT device, but feel free to pick anything that can run Python and can talk to the Internet. There are certain bits and pieces of the setup that you will have to go through though:

Here is what we are going to do:

1. Use a third party Alexa skill (ASK) to route certain Alexa interactions (intents) to your device - using a special invocation
2. Use a AWS Lambda function as a forwarder between Alexa and your device (they are bits of nicely formatted and well-defined JSON)
3. You will create a "thing" on AWS IoT to represent your IoT device
4. The Python Lambda function will use MQTT (add link) to securely communicate with your device using AWS IoT - no need to change it
5. You will use a Python client on your home device to listen for messages from our Lambda function and parse the forwarded Alexa intents
6. Everything was building up to this point, since now you can handle the Alexa intent on your device, and the best bit is that you can immediately send a reply, which will be forwarded back to Alexa and magic! The Echo will reply you.

New to programming, or Python? Checkout the `15 minute mini-intro`_!

.. _`Alexa Skills Kit`: https://developer.amazon.com/alexa-skills-kit
.. _`official ASK starter guide`: https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/getting-started-guide
.. _`AWS Lambda`: https://aws.amazon.com/lambda/details/
.. _`low cost`: https://aws.amazon.com/lambda/pricing/
.. _`here`: https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/developing-an-alexa-skill-as-a-lambda-function
.. _`flask-ask package`: https://github.com/johnwheeler/flask-ask
.. _`developer account`: https://developer.amazon.com/
.. _`AWS account`: https://aws.amazon.com/
.. _`the first million AWS Lambda calls are free`: https://aws.amazon.com/lambda/pricing/
.. _`15 minute mini-intro`: https://github.com/means-to-meaning/FirstAlexaSkills/tree/master/docs/python_intro.rst