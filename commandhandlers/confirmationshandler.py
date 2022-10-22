#!/usr/bin/env python

import datetime
import logging
from sqlite3 import IntegrityError

from config import strings
from dal import datamanager
from messaging import messageparser

logger = logging.getLogger()


def handle_message_content(sender, message_content):
    handling_functions = {'dodaj': _handle_add,
                          'wyslano': _handle_sent_confirmation,
                          'wysłano': _handle_sent_confirmation,
                          'otrzymano': _handle_received_confirmation}

    command = messageparser.get_command_from(message_content).lower()

    try:
        return handling_functions[command](sender)
    except KeyError:
        logger.info('Got unknown command')
        return strings.help_text


def _handle_sent_confirmation(sender):
    logger.info('Got sent confirmation')

    try:
        logger.info('Trying to save sent confirmation for user: ' + sender)

        participants = datamanager.get_participants()
        if sender not in participants:
            return strings.not_a_participant

        datamanager.save_send_confirmation(sender, datetime.datetime.now())
    except IntegrityError:
        logger.warning('Duplicated sent confirmation')
        return strings.confirmation_already_exists
    except Exception as exc:
        logger.warning('Sent confirmation saving failed. Reason: ' + str(exc))
        return strings.error_text
    else:
        logger.info('Sent confirmation saved')
        return strings.sent_confirmation_saved


def _handle_received_confirmation(sender):
    logger.info('Got received confirmation')

    try:
        logger.info('Trying to save received confirmation for user: ' + sender)

        participants = datamanager.get_participants()
        if sender not in participants:
            return strings.not_a_participant

        datamanager.save_received_confirmation(sender, datetime.datetime.now())
    except IntegrityError:
        logger.warning('Duplicated received confirmation')
        return strings.confirmation_already_exists
    except Exception as exc:
        logger.warning('Received confirmation saving failed. Reason: ' + str(exc))
        return strings.error_text
    else:
        logger.info('Sent confirmation saved')
        return strings.received_confirmation_saved


def _handle_add(sender):
    return strings.data_gathering_disabled
