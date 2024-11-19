#!/usr/bin/env python

import datetime
import logging
from urllib.parse import urlparse
from sqlite3 import IntegrityError

from src.config import strings
from src.dal import datamanager
from src.messaging import messageparser


logger = logging.getLogger()


def handle_message_content(sender, message_content):
    handling_functions = {
        'dodaj': _handle_add_or_delete,
        'usuń': _handle_add_or_delete,
        'usun': _handle_add_or_delete,
        'wyslano': _handle_sent_confirmation,
        'wysłano': _handle_sent_confirmation,
        'nadano': _handle_sent_confirmation,
        'otrzymano': _handle_received_confirmation,
        'odebrano': _handle_received_confirmation,
        'odebrane': _handle_received_confirmation,
        'otrzymałam': _handle_received_confirmation,
        'otrzymałem': _handle_received_confirmation,
        'otrzymalam': _handle_received_confirmation,
        'otrzymalem': _handle_received_confirmation,
    }

    command = messageparser.get_command_from(message_content).lower()
    arguments = messageparser.remove_command_from(message_content)

    try:
        return handling_functions[command](sender, arguments)
    except KeyError:
        logger.warning(f'Got unknown command: {command}')
        return [(sender, strings.help_text)]


def _handle_sent_confirmation(sender, arguments=None):
    logger.info(f'Got sent confirmation from: {sender}')

    try:
        logger.info(f'Trying to save sent confirmation')

        if not datamanager.is_participant(sender):
            return [(sender, strings.not_a_participant)]

        tracking_url = None
        if arguments:
            logger.debug('Confirmation has parameter')
            if _is_url(arguments):
                tracking_url = arguments
                logger.debug(f'Tracking URL detected: {tracking_url}')
            else:
                logger.warning(f'Confirmation parameter is not valid URL: {arguments}')

        datamanager.save_send_confirmation(sender, datetime.datetime.now(), tracking_url)

    except IntegrityError:
        logger.warning('Duplicated sent confirmation')
        return [(sender, strings.confirmation_already_exists)]
    except Exception as exc:
        logger.error(f'Sent confirmation saving failed. Reason: {str(exc)}')
        return [(sender, strings.error_text)]
    else:
        logger.info('Sent confirmation saved')
        gift_receiver = datamanager.get_gift_receiver_from(sender)
        answers = [
            (sender, strings.sent_confirmation_saved),
            (gift_receiver, strings.package_sent_notification),
        ]

        if tracking_url:
            answers.append((gift_receiver, f"{strings.tracking_url_text}: {tracking_url}"))

        return answers


def _handle_received_confirmation(sender, _):
    logger.info('Got received confirmation')

    try:
        logger.info(f'Trying to save received confirmation for user: {sender}')

        if not datamanager.is_participant(sender):
            return [(sender, strings.not_a_participant)]

        datamanager.save_received_confirmation(sender, datetime.datetime.now())
    except IntegrityError:
        logger.warning('Duplicated received confirmation')
        return [(sender, strings.confirmation_already_exists)]
    except Exception as exc:
        logger.error(f'Received confirmation saving failed. Reason: {str(exc)}')
        return [(sender, strings.error_text)]
    else:
        logger.info('Received confirmation saved')
        gift_sender = datamanager.get_gift_sender_for(sender)

        if not datamanager.has_send_confirmation(gift_sender):
            _automatic_mark_as_send(gift_sender)

        return [
            (sender, strings.received_confirmation_saved),
            (gift_sender, strings.package_received_notificaton)
        ]


def _handle_add_or_delete(sender, _):
    return [(sender, strings.data_gathering_disabled)]


def _automatic_mark_as_send(sender):
    logger.warning(f'Marking package from {sender} as sent')
    _handle_sent_confirmation(sender)


def _is_url(text):
    result = urlparse(text)
    if result.scheme and result.netloc:
        return True
    else:
        return False
