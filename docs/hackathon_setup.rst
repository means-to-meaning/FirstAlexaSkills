=========================================
Skillathon - a hackathon for Alexa Skills
=========================================

PC Setup for the skillathon
===========================

1. Create an Amazon developer account and an AWS account for the event. Follow the steps outlined in the 'Setup and requirements' section of the `README`_.

2. Check that you have a working internet connection

   .. code-block:: console

       $ ping google.com

3. Install IDE and dependencies on the PC

   .. code-block:: console

       $ sudo apt-get update && sudo apt-get upgrade
       $ sudo apt-get install python3.6 python3-pip python3-dev idle
       $ sudo pip3 install --upgrade pip
       $ sudo pip3 install firstalexaskills jupyter nose
       $ aws configure --profile lambdaUser # use the API credentials from AWS
       test the setup:
       $ aws lambda list-functions --profile lambdaUser # there should be a list (possibly empty) of functions
       $ unpack_example_skills
       $ jupyter notebook ~/example_skills/python_intro/python_intro.ipynb # does the notebook work?
       $ rm -rv example_skills

4. Depending on the experience level of the participants, you might decide to define the Alexa skills in advance, in order to save time and focus on coding, rather than filling out forms. Each ASK Alexa skill needs to have a single service endpoint. Therefore each team developing a Lambda service will require an Alexa skill of their own.

   Note: It can be practical to create a list of team names based on the expected number of attendees before the event. Define a skill in the development portal and use the team name as the name of the skill. That way, during the main event, the participants don't have to interact with the developer.amazon.com portal at all. Each team can then invoke the skill saying: "Alexa, ask team blue to tell me something". Please follow Alexa's advice on suitable words for skill invocation when using this! Similarly, each team will need to use their team name as part of the AWS Lambda function name they will create.

5. Finally, pair your Alexa devices (Echo, Echo Dot, Echo Show) with the Amazon developer account you've created and test the whole setup.

Things to consider
==================
**Problem:**

* Echo's speech recognition accuracy decreases in proportion to the distance of the speaker and amount of noise in the room. A large room full of people screaming gentle conversation invitations to multiple Alexa devices at once can result into a painful experience.

**Workaroud:**

* Rely more on software testing and limit the Echo interactions for the final "ahaaa" moments rather than continuous testing
* Split teams into smaller rooms

**Problem:**

* The Alexa devices require wifi to communicate with Alexa and many wifi devices (smartphones etc.) trying to connect concurrently to the same network can make the interactions more sluggish, or outright stall them.

**Workaroud:**

* Simples, dedicate a wifi for the Alexa devices and consider not using other wifi access points on the premises to avoid signal interference.

Agenda for the skillathon
=========================
In order for the participants to have fun and make the most of their creative ideas, they will need three things: Python basics, a conceptual idea of how Alexa skills work and tools to code and test the skills.

1. Intro to Alexa and third-party Alexa skills (ASK)

2. Intro to Python (note: consider to split the participants into groups for people with and without coding experience). People that understand the concept of variables and functions should work through the Intro to Python notebook. People that don't know those concepts or haven't programmed before should first get an explanation of what programs are, what is execution flow and how variables and functions work. (see the `15 minute Intro to Python for non-programmers`_)

   .. code-block:: console

       $ cd ~
       $ unpack_example_skills # will create a directory alexa_skills with skills and resources
       $ jupyter notebook ~/example_skills/python_intro/python_intro.ipynb

3. Quick demo of a working Alexa skill
4. Split into teams and choose a team name
5. Work through the `AlexaFirstSkills tutorial`_

.. _`AlexaFirstSkills tutorial`: https://github.com/means-to-meaning/FirstAlexaSkills/blob/master/docs/tutorials.rst
.. _`15 minute Intro to Python for non-programmers`: https://github.com/means-to-meaning/FirstAlexaSkills/tree/master/docs/python_intro.rst
.. _`README`: https://github.com/means-to-meaning/FirstAlexaSkills/tree/master/README.rst
