#!/usr/bin/env python

import logging

from src.config import strings
from src.dal import datamanager
from src.messaging import messageparser


logger = logging.getLogger()


def handle_message_content(sender, message_content):
    handling_functions = {
        'dodaj': _handle_add,
        'usuń': _handle_delete
    }

    command = messageparser.get_command_from(message_content).lower()
    arguments = messageparser.remove_command_from(message_content)

    try:
        return handling_functions[command](sender, arguments)
    except KeyError:
        logger.warning(f'Got unknown command: {command}')
        return [(sender, strings.help_text)]


def _handle_add(sender, user_data):
    logger.info('Got add command')

    try:
        logger.info(f'Trying save data for user: {sender}')
        datamanager.save_user_data(sender, user_data)
    except Exception as exc:
        logger.error(f'Data saving failed. Reason: {str(exc)}')
        return [(sender, strings.error_text)]
    else:
        logger.info('User data saved')
        return [(sender, strings.data_saved)]


def _handle_delete(sender, _):
    logger.info('Got delete command')

    try:
        logger.info(f'Trying delete data for user: {sender}')

        if datamanager.is_participant(sender):
            datamanager.delete_user_data(sender)
        else:
            logger.info(f'User {sender} is not a participant.')
            return [(sender, strings.not_a_participant)]
    except Exception as exc:
        logger.error(f'Data deletion failed. Reason: {str(exc)}')
        return [(sender, strings.error_text)]
    else:
        logger.info('User data deleted')
        return [(sender, strings.data_deleted)]
