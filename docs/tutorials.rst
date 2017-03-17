Examples on creating Alexa third-party skills
---------------------------------------------


Say something! (alexa_skill_saysomething)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Challenge:**
Create an Alexa third-party skill that you can tell a phrase: "Alexa, ask <my_skill_name> to say something!" and it replies: "I can say whatever you want me to say".

**Suggested steps:**

1. Start by creating a new directory where we will unpack the example Alexa skills

    .. code-block:: console

        $ mkdir alexa_development
        $ unpack_example_skills
        $ cd example_skills

2. Inside we will find three skills, including the saysomething skill

    .. code-block:: console

        $ cd alexa_skill_saysomething

3. The directory contains all you need to create your first Alexa skill. The file lambda_function.py contains the AWS Lambda code, lambda_test_data.json contains test data for generating fake Alexa events for testing. Start by opening lambda_function.py in your favourite Python editor and try to follow the execution flow which starts in the function lambda_handler().

4. By now you you should be completely confused and frustrated from staring at incomprehensible code logic dealing with some uknown objects called event and intent. So here is what is going on: Imaging you tell the Echo something like 'Alexa, ask magic skill to say something'. Your Alexa skill (which isn't created yet but will be in a few steps) will be used to convert the words 'say something' to an 'intent'. Alexa will then send this 'intent' to your AWS Lambda function which will process it, and send a reply within seconds back to Alexa. Ok, this is still a lot to process. It's enough for now if you understand two things: A. In your Alexa skill, you will define which sentences (utterances) correspond to which intents. B. When you speak to an Echo, the AWS Lambda function (the Python code you've been looking at) will receive an intent and will process it.

5. We can upload the function as is to the cloud to make sure all works as expected. When we run create_lambda_function, it will zip up this directory, send it to the cloud and test it using 3 separate Alexa events. TODO: add script to print events using testdata to the console

    .. code-block:: console

        $ create_lambda_function --function-name saysomething --dir .
        Function succesfully created!
        AWS Lambda function ARN: arn:aws:lambda:eu-west-1:your_account_id:function:saysomething
        Testing function now!
        Sending Alexa Intent: FakeIntent and slots:{}
        There was an error:
        'response'
        Sending Alexa Intent: AskIntent and slots:{}
        Alexa replied: I say whatever I please
        Sending Alexa Intent: AskIntent and slots:{}
        Alexa replied: I say whatever I please

6. Now we can register a third-party Alexa skill using the Alexa Skills Kit (see this `step by step guide`_). We will only create the skill for testing purposes and will not submit it to the store. The skill directory contains data for the interaction model. intent_schema.json contains the intent schema and utterances.txt contain a single sample utterances. You will need to copy both of them in the appropriate fields. You will need the following information:
    - Skill Information
        - Skill Type: Custom
        - Application Id: make one up
        - Name: make one up
        - Invocation Name: make one up
    - Interaction Model
        - Intent Schema: copy&paste contents of intent_schema.json
        - Sample Utterances: copy&paste contents of utterances.txt
    - Configuration
        - Service Endpoint Type: AWS Lambda ARN (Amazon Resource Name)
        - Pick a geographical region that is closest to your target customers: you have to pick the region where you created the AWS Lambda function (if you followed our setup, this region will be eu-west-1, Europe) copy&paste the AWS Lambda function ARN from the create_lambda_function console output
    - Test
        - Service Simulator: type in a sentence to simulate speaking to an Alexa device - 'say something' and check out the reply. If you see a reply appearing, you can use an Alexa device such as an Echo, or Dot to test the skill as well. The device needs to be paired with the same account we used for developing this skill.

7. Go through the execution flow of our lambda_function.py again, but this time pay special attention to the on_intent() function. We will modify the variable 'speech_output' so that Alexa replies: 'I can say whatever you want me to say'

    .. code-block:: console

        $ <YOUR_FAV_EDITOR_HERE> lambda_function.py

8. Once we are satisfied with the local changes we need to update the Lambda in the cloud and test it

    .. code-block:: console

        $ update_lambda_function --function-name saysomething --dir .

9. If you have an Echo, you can talk to your skill now! Otherwise you will have to make due with the Simulator. If the reply is 'I can say whatever you want me to say', then you should congratulate yourself. You have just created and modified your first Alexa skill! Now see whether you can modify the skill to say something else.


What's cool? (alexa_skill_whatscool)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Challenge:**
Teach Alexa about what is cool. Currently the example skill chooses randomly between three replies what is the coolest movie ever. Can you teach it what are some other cool things? (bands?  food?)

**Suggested steps:**
TODO: add steps

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

.. _`step by step guide`: https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/registering-and-managing-alexa-skills-in-the-developer-portal