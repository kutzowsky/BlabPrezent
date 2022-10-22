#!/usr/bin/env python

import configparser
import logging

from config.BotConfiguration import BotConfiguration

logger = logging.getLogger()


def get_bot_configuration(config_file_path='configuration.ini'):
    config_parser = configparser.ConfigParser()
    dataset = config_parser.read(config_file_path)

    if len(dataset) == 0:
        raise FileNotFoundError('Configuration file {} not found'.format(config_file_path))

    bot_configuration = BotConfiguration()
    bot_configuration.jid = config_parser.get('Connection', 'jid')
    bot_configuration.password = config_parser.get('Connection', 'password')  # i know, i know #todo do it better
    bot_configuration.blabler_bot_jid = config_parser.get('Connection', 'blabler_bot_jid')

    bot_configuration.website_login = config_parser.get('Connection', 'website_login')
    bot_configuration.website_password = config_parser.get('Connection', 'website_password')

    logger.info('Configuration loaded from: ' + config_file_path)

    return bot_configuration
