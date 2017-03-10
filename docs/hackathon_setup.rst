Skillathon - a hackathon for Alexa Skills
=========================================

Setup for the skillathon
~~~~~~~~~~~~~~~~~~~~~~~~
1. Install IDE and dependencies on the PC

    .. code-block:: console

        $ sudo apt-get install screen python2.7 python-pip python-dev ipython ipython-notebook idle
        $ sudo pip install --upgrade pip
        $ sudo pip install FirstAlexaSkills jupyter nose

2. Create an Amazon developer account and an AWS account for the event. Follow the steps outlined in the 'Setup and requirements' section of the `README`_.

3. Depending on the experience level of the participants, you might decide to create the skills and corresponding Lambda functions in advance, in order to allow the participants to focus on modifying them, rather than spend time with the skill setup. Create a list of team names based on the expected number of attendees.

4.  Create a Lambda function for each team and each skill you want to use. Example SaySomething skill:

    .. code-block:: console

        $ cd ~/
        $ unpack_example_skills
        $ cd example_skills/alexa_skill_saysomething
        $ create_lambda_function --function-name saysomething_<TEAM_NAME> --dir .

5. Define a skill in the development portal and use <TEAM_NAME> and a number for which skill to use. Example: For the team 'blue' and first skill you will be showing, the invocation name can be 'blue one'. The scheme is really up to you, but it will need to be unique, self-explanatory and follow the ASK guidelines for invocations. Use the <TEAM_NAME> to name the skill as well and set the right ARN as the endpoint.

6. Pair an Alexa device (Echo, Dot) with the Amazon developer you've created and test the whole setup.

Agenda for the skillathon
~~~~~~~~~~~~~~~~~~~~~~~~~

1. Intro to Python (split into groups for people with and without coding experience). People that understand the concept of variables and functions should work through the Intro to Python notebook. People that don't know the concept or haven't programmed before should first get an explanation of what programs are, what is execution flow and how variables and functions work. (see the `15 minute Intro to Python for non-programmers`_)

    .. code-block:: console

        $jupyter notebook ~/alexa_skills/python_intro/python_intro.ipynb

2. Quick demo of the SaySomething, FactFinding and IoT skills so everybody sees/hears how they work
3. Split into teams and choose a team name
4. The skills and Lambda functions are already created for all teams. Test your skill using an Echo, or the Simulator in the developer portal. Each team's Alexa invocation will be "team <colour>". Example of team blue invoking the first skill (SaySomething): Alexa, ask blue one, to say something.
5. Modify the SaySomething code to say something... else:

    .. code-block:: console

        $ cd ~/alexa_skills/alexa_skill_saysomething
        $ idle example_skills/alexa_skill_saysomething/lambda_function.py

6. Update and test the SaySomething AWS Lambda function

    .. code-block:: console

        $ cd ~/alexa_skills/alexa_skill_saysomething
        $ update_lambda_function --function-name saysomething --dir .

7. Test the skill using an Echo, or the Amazon dev portal simulator as before.

8. Repeat steps 4. - 7.  for any other skills you've setup.

.. _`15 minute Intro to Python for non-programmers`: https://github.com/means-to-meaning/FirstAlexaSkills/tree/master/docs/python_intro.rst
.. _`README`: https://github.com/means-to-meaning/FirstAlexaSkills/tree/master/README.rst