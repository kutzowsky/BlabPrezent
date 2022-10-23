#!/usr/bin/env python

import logging

from config import strings
from dal import datamanager
from messaging import messageparser

logger = logging.getLogger()


def handle_message_content(sender, message_content):
    handling_functions = {'dodaj': _handle_add}

    command = messageparser.get_command_from(message_content).lower()
    arguments = messageparser.remove_command_from(message_content)

    try:
        return handling_functions[command](sender, arguments)
    except KeyError:
        logger.info('Got unknown command')
        return [(sender, strings.help_text)]


def _handle_add(sender, user_data):
    logger.info('Got add command')

    try:
        logger.info('Trying save data for user: ' + sender)
        datamanager.save_user_data(sender, user_data)
    except Exception as exc:
        logger.warning('Data saving failed. Reason: ' + str(exc))
        return [(sender, strings.error_text)]
    else:
        logger.info('User data saved')
        return [(sender, strings.data_saved)]
