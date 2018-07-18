===================================================
Examples of creating Alexa third-party skills (ASK)
===================================================


First Alexa Skill (alexa_skill_first)
=====================================

**Challenge:**
Create your first Alexa third-party skill with the following features:

1. Tell Alexa a specific phrase: "Alexa, ask <my_skill_name> to say something!" and get back a reply of your choice: "I can say whatever you want me to say".
2. Personalize your skill by teaching it facts about your friends: "Alexa, tell me something about <person's name>." and get back a reply: "<person's name> is crazy for pancakes with chocolate and banana."
3. Create a random generator of facts about cool subjects: "Alexa, tell me something cool about <subject>." and get back a random piece of trivia about <subject>: "

To accomplish the above, we will use a working skill which we will deploy to AWS, test and later modify. Rather than start of by learning all the details about AWS Lambda and the Alexa service APIs, we will focus on a simple, but reliable workflow that will allow us to develop much more complex Alexa skills later on.

**Before we start:**

Let's stop and think how can we do what the challenge is asking for. We will need to create three intents (saying something, person facts, subject trivia), a mapping for sentences and intents and also define some variables (name of the person, etc.) that Alexa needs to pass us alongside the intent name. We will need to create a third-party Alexa skill using ASK and we will also need a service, that will process the intents and generate replies for them. Our example skill comes with all the resources required to define an Alexa skill using ASK - utterances.txt, intent_schema.json. It also comes with working code for the webservice (AWS Lambda) - lambda_function.py. It also comes with tests, test cases and command-line tools that will allow us to easily modify the existing skill code. Let's dive in!

**Suggested steps:**

   .. image:: https://github.com/means-to-meaning/FirstAlexaSkills/blob/master/docs/alexa_skill.svg
        :align: center

Deploy and test an existing skill (green boxes)
-----------------------------------------------

1. Start by creating a new directory where we will unpack the example Alexa skills

   .. code-block:: console

        $ unpack_example_skills
        $ cd example_skills

2. Inside we will find two skills, and some additional resources for our Alexa development. Let's have a look at our first skill:

   .. code-block:: console

        $ cd alexa_skill_first

3. The above directory contains all you need to create your first Alexa skill. The only file we will focus on at this stage is lambda_function.py, which contains the AWS Lambda code. Start by opening lambda_function.py in an editor (we will be using IDLE for this tutorial) and try to follow the execution flow which starts in the function lambda_handler().

   .. code-block:: console

        $ idle lambda_function.py

4. The first look at lambda_function.py can be confusing since the code is dealing with some objects called "event" and "intent". To understand what they are and when is this code executed, let's look at what happens when you speak to Alexa:

   .. image:: https://m.media-amazon.com/images/G/01/DeveloperBlogs/AmazonDeveloperBlogs/legacy/adiag._CB520201042_.png
        :align: center

   (Source: `Alexa blogs`_)

   You tell the Echo something like 'Alexa, ask magic skill to say something'. Your "magic skill" (a third-party Alexa skill) will be used to convert the words 'say something' to a particular intent, let's call it the "saySomethingIntent". Alexa will then trigger your AWS Lambda function in the cloud and supply it with the intent object containing the data of your "saySomethingIntent". Your AWS Lambda function (the code in lambda_function.py) will process the intent according to your own logic (defined in lambda_function.py) and send a reply in a within seconds back to Alexa. Ok, this is still a lot to process. It's enough for now if you understand two things:

   A. In your Alexa skill definition (on developer.amazon.com), you will define which sentences (utterances) correspond to which intents.

   B. When you speak to Alexa, the AWS Lambda function (the Python code you've been looking at) will receive a specific intent that the sentence triggered and will process it.

(you can close the IDLE window now)

5. We can upload the function as is to the cloud to make sure all works as expected. When we run create_lambda_function, it will zip up this directory and send it to the cloud. We will need the "AWS Lambda function ARN" identifier later to link our skill definition to our processing function.

   .. code-block:: console

        $ create_lambda_function --function-name skill_first --dir .
        Function successfully created!
        AWS Lambda function ARN: arn:aws:lambda:<your_aws_region>:<your_account_id>:function:skill_first

6. Our Lambda function is now in the cloud, ready to be executed. Let's make sure we can indeed run it. One neat way to test our AWS Lambda functions is to generate fake Alexa intents and send them to AWS Lambda. This allows us to skip speaking to an Echo and to automate our tests. We generate a specific intent and send it to our AWS Lambda function as if we were the Alexa service, and in return we will get the text reply the Alexa service would receive. For an example intent json object see: `event_template.json`_. The AlexaFirstSkills package allows us to create these test events by modifying selected fields of the intent object, such as the "name", or any variables ("slots"). Let's have a quick look at our test events:

   .. code-block:: console

        $ cat tests/data/lambda_test_data.json

7. Our tests generate 3 different types of intents. We can generate the events and send them to AWS Lambda using test_lambda_function commandline script.

   .. code-block:: console

        $ test_lambda_function --function-name skill_first --test-data tests/data/lambda_test_data.json

   The tests print the intent and slots sent to our AWS Lambda function and the generated reply. Let's look at them step by step:

   .. code-block:: console

        ############################################
        Testing function now!
        ############################################
        Sending Alexa Intent: FakeIntent and slots:{}
        Lambda function replied: hmm not sure how to deal with your request

   The first test just checks what happens if we send Lambda an intent that it doesn't recognize, we chose the arbitrary name "FakeIntent". It is reassuring to by default, the function would send a meaningful reply back to Alexa. A situation like this can easily occur if you add a skill to your ASK definition without adjusting the Lambda skill functionality.

   .. code-block:: console

        Sending Alexa Intent: saySomethingIntent and slots:{}
        Lambda function replied: I say whatever I please

   Our first test of an existing intent shows that Lambda generates a proper reply. Our first task for this coding challenge involves changing this reply to a string of our choice. Once we have a definition of our skill on developer.amazon.com, we can test this skill out by telling Echo, "Alexa, say something" and Alexa will reply: "I say whatever I please". At that point we won't be surprised however, since we already tested and proved here that the intent handling works!

   .. code-block:: console

        Sending Alexa Intent: personalFactIntent and slots:{}
        Lambda function returned an error:
           stackTrace:
         /var/task/lambda_function.py
         208
         lambda_handler
         return on_intent(event['request'], event['session'])

         /var/task/lambda_function.py
         170
         on_intent
         return intent_handler(intent, session)

         /var/task/lambda_function.py
         63
         intent_handler
         person_name = intent['slots']['Person']['value']
           errorMessage: 'Person'
           errorType: KeyError

        Lambda function didn't reply!!!

   Wow! This clearly doesn't look good. Let's try to understand what's going on here. We are sending Lambda a personalFactIntent without any slots. Translated into human, we are supposed to ask Alexa: "Alexa, tell me something about a <NAME>". The problem is that the way our lambda function is written currently, it expects a <NAME> for this intent, which should be passed as a slot variable (is this a good idea? could we fix that??). What we are seeing as a result is the error message from Python ("stack trace") that complains the key "Person" not being present in the intent['slots'] dictionary.

   While this is a long and ugly message, this example really shows the value of testing your Lambda function. Rather than just writing our Lambda function and then asking Echo a dozen different questions to check whether the skill works, we can define any situation we would like via the tests/data/lambda_test_data.json and get back the exact reply we would get in spoken language from Alexa. Just fyi, in the above case, if we try this with an Echo: "Alexa, tell me something about", we will get back only silence, as the Lambda function isn't handling this case well at all and errors out before passing a reply to Alexa.

   **Extra credit:**
   There are at least two ways to fix this. a/ We don't assume the "Person" key will always be present for this intent, that means we add a check for it. b/ It would be really good to add a default reply if things go south, just like we did for the case when Lambda receives an unknown intent. Unexpected problems in Python usually trigger an exception, which causes the program to stop immediately. One thing every skill should consider is to catch these exceptions and rather than simply throw an error, send a default reply to the user notifying them that you cannot provide an answer at this time due to an error.


   .. code-block:: console

        Sending Alexa Intent: personalFactIntent and slots:{u'Person': {u'name': u'personalFactIntent', u'value': u'robogals'}}
        Lambda function replied: robogals was founded in 2008 in melbourne, australia

   We don't need to bother with fixing the Lambda error handling right now. We can simply add a "Person" variable into our test and everything works just fine. The above test corresponds to the utterance: "Alexa, tell me something interesting about `Robogals`_".

   .. code-block:: console

        Sending Alexa Intent: whatsCoolIntent and slots:{u'Subject': {u'name': u'whatsCoolIntent', u'value': u'movie'}}
        Lambda function replied: Lord of the rings

   Our last test checks whether the "whatsCoolIntent" works correctly. One cool thing about this intent is that it always returns a slightly different answer, so don't be surprised if you see a different movie on your output.

   Equipped with the test_lambda_function script and our test definitions in tests/data/lambda_test_data.json, we can confidently go into changing the lambda functionality as we have a simple way to check we are on the right track. In addition to testing the entire Lambda function, we can also test individual bits of Python functionality locally before uploading it to AWS Lambda - we will see more about that later. But now, let's define our skill!

8. We can register a third-party Alexa skill using the Alexa Skills Kit (see this `step by step guide`_). We will only create the skill for testing purposes and will not submit it to the store. The skill directory contains data for the interaction model. intent_schema.json contains the intent schema and `utterances.txt`_ contain a single sample utterances. You will need to copy both of them in the appropriate fields. You will need the following information:

   - Skill Information
      - Skill Type: Custom
      - Application Id: make one up
      - Name: make one up
      - Invocation Name: make one up
   - Interaction Model
      - Intent Schema: copy&paste contents of intent_schema.json
      - Sample Utterances: copy&paste contents of `utterances.txt`_
   - Configuration
      - Service Endpoint Type: AWS Lambda ARN (Amazon Resource Name)
      - Pick a geographical region that is closest to your target customers: you have to pick the region where you created the AWS Lambda function (if you followed our setup, this region will be eu-west-1, Europe) copy&paste the AWS Lambda function ARN from the create_lambda_function console output
   - Test
      - Service Simulator: type in a sentence to simulate speaking to an Alexa device - 'say something' and check out the reply. If you see a reply appearing, you can use an Alexa device such as an Echo, or Dot to test the skill as well. The device needs to be paired with the same account we used for developing this skill.

9. Test the newly created Alexa skill with a physical device - for example with an `Echo Dot`_. You can invoke the individual skills using any of the utterances we used in our ASK definition (see `utterances.txt`_). The device should give the replies currently coded in lambda_function.py as we have seen during our AWS Lambda testing.

   If you don't have an Alexa device, you can easily test your skill through the developer.amazon.com portal - navigate to where you defined your skill and go the the Test section. You can type a sentence and you should receive text reply from Alexa.

**What did we learn?**

* We have deployed and tested an AWS Lambda function for our skill
* We have seen how speech translates into intents and how intents are processed in Python
* We have defined our Alexa skill using ASK and tested it works

Develop and update skill (blue boxes)
-------------------------------------

1. The toughest part of Alexa skill creation - the setup, is done and you can give yourself a pet on the back. Now we will turn our attention to modifying the skill. We will do this by first developing functionality and testing it locally. Then updating the AWS Lambda function (uploading the new code to AWS) and testing it using fake Alexa events.

   Let's go through the execution flow of our lambda_function.py again, but this time pay special attention to the intent_handler() function. It determines what to do based on the intent name we receive. Our first mission consists of modifying the reply to the "saySomethingIntent" and it will lead us to.. can you guess it?

   Yes, it will lead us to the get_something() function. If you have followed the Intro to Python notebook, you should be able to easily modify this function to return 'I can say whatever you want me to say'.

2. At this point, we could simply make the changes we want in lambda_function.py, upload it to the cloud and test it like we did before. But it is much more convenient to test lambda functions as much as we can locally (on our own computer) and only upload them once we are fairly certain our Python functions work. Easy enough, just like we passed fake Alexa events to our AWS Lambda function, we can call our Python functions locally and pass it different parameters. There is a set of tests for you in tests/test_lambda_unit.py.

3. Let's explore the local tests a bit before making any changes to our skill:

   .. code-block:: console

        $ idle tests/test_lambda_unit.py

   The first test, test_get_something(), simply calls the get_something() function from our lambda skill and checks using an "assert statement" that the function really returns what we would expect. If you haven't changed it, it should return "I say whatever I please".

   We can ran all of the tests at once and confirm that our current skill code works as expected (using nose or any other Python test framework):

   .. code-block:: console

        $ nosetests tests/test_lambda_unit.py
        ----------------------------------------------------------------------
        Ran 5 tests in 0.001s
        OK

4. Now that we know that our intent answering functions are working fine (to the extent we've tested them), we can modify get_something() in our code to return 'I can say whatever you want me to say':

   .. code-block:: console

        $ idle lambda_function.py

5. Once we make the change and save the file, it would be interesting to see what happens to our tests - one of them should no longer work since we have just changed the response get_something() is giving us and the test is still expecting to receive 'I say whatever I please'.

   .. code-block:: console

        $ nosetests tests/test_lambda_unit.py
        1 of the 5 tests should fail and show the Traceback

6. This is easy enough to fix, let's update the correct expected answer in our test_get_something() test and re-run all our local tests. This time, they should all pass again.

   .. code-block:: console

        $ idle tests/test_lambda_unit.py
        $ nosetests tests/test_lambda_unit.py
        ----------------------------------------------------------------------
        Ran 5 tests in 0.001s
        OK

7. Once we are satisfied with the local changes we can confidently update the Lambda in the cloud and test it

   .. code-block:: console

        $ cd alexa_skill_first
        $ update_lambda_function --function-name skill_first --dir .
        $ test_lambda_function --function-name skill_first --test-data tests/data/lambda_test_data.json

8. You can follow steps 4 to 7 to modify the remainder of your code and complete the rest of the challenge.

**What did we learn?**

* We have learned how to modify and locally test skill functionality

Where to go next?
-----------------
There is a couple of things you might consider as next steps:

* Add a new intent to this skill - remember you need to add it to both, the ASK definition and to lambda_function.py
* Check out some `example Alexa skills for beginners`_
* Have a look at Amazon's `documentation for creating Alexa skills`_
* Consider skill improvements - improved intent handling (check for dictionary keys before using them, etc.), error handling (catch exceptions, generate default answer), think about security (check skill application id), add more unit tests


Light on! (alexa_iot_skill)
===========================

**Challenge:**
Communicate with any Internet capable (IoT) device in your home through Alexa securely (no open ports in your firewall required), instantaneously (1-3 seconds to reach your device) and cheaply (both in terms of $$$ and kW/h). This can include anything from an Arduino to your PC.

**Overview**:

The goal of this example is to automate as much as possible behind the scenes and allow you to focus on your IoT logic, that means handling of the intents on the device and formulation of the replies. We will use MQTT for communicating messages between our AWS Lambda function and our device, use AWS IoT to keep track of devices and get access to a ton of additional functionality (like rules and notifications). We have selected a Raspberry Pi as our IoT device, but feel free to pick anything that can run Python and can talk to the Internet. There are certain bits and pieces of the setup that you will have to go through though:

Here is what we are going to do:

1. Use a third party Alexa skill (ASK) to route certain Alexa interactions (intents) to your device - using a special invocation
2. Use a AWS Lambda function as a forwarder between Alexa and your device (they are bits of nicely formatted and well-defined JSON)
3. You will create a "thing" on AWS IoT to represent your IoT device
4. The Python Lambda function will use MQTT (add link) to securely communicate with your device using AWS IoT - no need to change it
5. You will use a Python client on your home device to listen for messages from our Lambda function and parse the forwarded Alexa intents
6. Everything was building up to this point, since now you can handle the Alexa intent on your device, and the best bit is that you can immediately send a reply, which will be forwarded back to Alexa and magic! The Echo will reply you.

.. _`event_template.json`: https://github.com/means-to-meaning/FirstAlexaSkills/blob/master/src/FirstAlexaSkills/data/event_template.json
.. _`utterances.txt`: https://github.com/means-to-meaning/FirstAlexaSkills/blob/master/example_skills/alexa_skill_first/utterances.txt
.. _`Robogals`: http://robogals.org/
.. _`Echo Dot`: https://en.wikipedia.org/wiki/Amazon_Echo#Amazon_Echo_Dot
.. _`step by step guide`: https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/registering-and-managing-alexa-skills-in-the-developer-portal
.. _`Alexa Blogs`: https://developer.amazon.com/blogs/alexa/post/Tx33L8B84PQ17FB/an-introduction-to-the-alexa-skills-kit-ask
.. _`example Alexa skills for beginners`: https://developer.amazon.com/alexa-skills-kit/alexa-skills-developer-training
.. _`documentation for creating Alexa skills`: https://developer.amazon.com/alexa-skills-kit
