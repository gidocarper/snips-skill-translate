#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
from hermes_python.hermes import Hermes, MqttOptions
import io
from translate import Translator
import toml

USERNAME_INTENTS = "mcitar"
MQTT_BROKER_ADDRESS = "localhost:1883"
MQTT_USERNAME = None
MQTT_PASSWORD = None


def add_prefix(intent_name):
    return USERNAME_INTENTS + ":" + intent_name


def read_configuration_file():
    try:
        cp = configparser.ConfigParser()
        with io.open("config.ini", encoding="utf-8") as f:
            cp.read_file(f)
        return {section: {option_name: option for option_name, option in cp.items(section)}
                for section in cp.sections()}
    except (IOError, configparser.Error):
        return dict()


def intent_callback_translate(hermes, intent_message):
    hermes.publish_end_session(intent_message.session_id, translator.translate(hermes, intent_message))

def intent_callback_get_text_to_translate(hermes, intent_message):
    hermes.publish_end_session(intent_message.session_id, translator.get_text_to_translate(hermes, intent_message, True))

def intent_callback_get_language(hermes, intent_message):
    hermes.publish_end_session(intent_message.session_id, translator.get_language(hermes, intent_message, True))



if __name__ == "__main__":
    config = read_configuration_file()
    translator = Translator(config)

    snips_config = toml.load('/etc/snips.toml')
    if 'mqtt' in snips_config['snips-common'].keys():
        MQTT_BROKER_ADDRESS = snips_config['snips-common']['mqtt']
    if 'mqtt_username' in snips_config['snips-common'].keys():
        MQTT_USERNAME = snips_config['snips-common']['mqtt_username']
    if 'mqtt_password' in snips_config['snips-common'].keys():
        MQTT_PASSWORD = snips_config['snips-common']['mqtt_password']
    mqtt_opts = MqttOptions(username=MQTT_USERNAME, password=MQTT_PASSWORD, broker_address=MQTT_BROKER_ADDRESS)

    with Hermes(mqtt_options=mqtt_opts) as h:
        h.subscribe_intent(add_prefix("translate"), intent_callback_translate)
        h.subscribe_intent(add_prefix("getTextToTranslate"), intent_callback_get_text_to_translate)
        h.subscribe_intent(add_prefix("getLanguage"), intent_callback_get_language)
        h.start()
