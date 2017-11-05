#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import logging

from config.BotConfiguration import BotConfiguration

_CONFIG_LOCATION = 'configuration.ini'

logger = logging.getLogger()

def get_bot_configuration():
    config_parser = ConfigParser.ConfigParser()
    config_parser.read(_CONFIG_LOCATION)

    bot_configuration = BotConfiguration()
    bot_configuration.jid = config_parser.get('Connection', 'jid')
    bot_configuration.password = config_parser.get('Connection', 'password')  # i know, i know #todo do it better
    bot_configuration.blabler_bot_jid = config_parser.get('Connection', 'blabler_bot_jid')

    logger.info('Configuration loaded from: ' + _CONFIG_LOCATION)

    return bot_configuration
