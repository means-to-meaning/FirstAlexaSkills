import os
import json
import ast
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

script_dir = os.path.dirname(os.path.realpath(__file__))

fake_tempstatus_fn = os.path.join(script_dir, "light_state.txt")


def light(cmd):
    reply = ""
    if cmd == "on":
        reply = ""
    elif cmd == "off":
        reply = ""
    elif cmd == "status":
        reply = "The light shall bring victory"
    else:
        reply = ""
    return reply


def get_temperature():
    logger = logging.getLogger(__name__)
    temp = ""
    if not os.path.exists(fake_tempstatus_fn):
        temp = "not set"
    else:
        with open(fake_tempstatus_fn, 'r') as temp_storage:
            temp = temp_storage.readline().strip()
            logger.info("Getting temperature: " + str(temp))
    return temp


def set_temperature(temp):
    logger = logging.getLogger(__name__)
    with open(fake_tempstatus_fn, 'w') as temp_storage:
        logger.info("Setting temperature to: " + str(temp))
        temp_storage.write(str(temp))


def temperature(temp=None):
    min_temp = 15
    max_temp = 27
    if temp:
        temp = int(temp)
        # Always sanity check the inputs Alexa sends us!
        if temp < max_temp and temp > min_temp:
            set_temperature(temp)
            reply = "Temperature set to " + str(temp)
        else:
            reply = "Invalid temperature setting"
    else:
        cur_temp = str(get_temperature())
        reply = "Current temperature is " + cur_temp
    return reply


def process_intent(msg):
    logger = logging.getLogger(__name__)
    # TODO: find a way to replace ast.literal_eval() with json.loads()
    # which currently doesn't work since the received
    # Alexa msg contains single quotes and thus isn't recognized as valid json
    msg_dict = ast.literal_eval(msg.decode("utf-8"))
    intent = msg_dict["intent"]
    locale = msg_dict["locale"]
    request_id = msg_dict["requestId"]
    timestamp = msg_dict["timestamp"]
    type = msg_dict["type"]
    event_data = [str(intent), str(locale), str(request_id),
                  str(timestamp), str(type)]
    speech_output = ""
    logger.info("Received intent: " + ", ".join(event_data))
    if intent["name"] == "LightOnIntent":
        speech_output = light("on")
    elif intent["name"] == "LightOffIntent":
        speech_output = light("off")
    elif intent["name"] == "LightStatusIntent":
        speech_output = light("status")
    elif intent["name"] == "TemperatureSetIntent":
        slots = intent["slots"]
        temp = slots["Temperature"]["value"]
        speech_output = temperature(int(temp))
    elif intent["name"] == "TemperatureGetIntent":
        speech_output = temperature()
    else:
        speech_output = "hmm, your iot device doesn't support this intent yet"
    logger.info("Processed intent reply: " + str(speech_output))
    reply = {"speech_output": speech_output,
             "session_attributes": {},
             "reprompt_text": None,
             "should_end_session": True}
    msg_json = json.dumps(reply)
    return msg_json
