#!/usr/bin/env python

import logging

from . import messageparser
from commandhandlers import addinghandler as messagecontenthandler
# from commandhandlers import confirmationshandler as messagecontenthandler
from config import strings

logger = logging.getLogger()


def handle(message):
    if not messageparser.is_directed(message):
        return None

    sender = messageparser.get_sender_from(message)
    answers = None

    if messageparser.is_directed_private(message):
        logger.info('Directed private message: ' + message)

        message_content = messageparser.get_content_from(message)
        answers = messagecontenthandler.handle_message_content(sender, message_content)

    if messageparser.is_directed_public(message):
        logger.debug('Directed public message: ' + message)
        logger.debug('Sending warning')
        answers = [(sender, strings.public_message_warn)]

    answers_text = map(_create_private_message_text, answers)
    return answers_text


def _create_private_message_text(message_tuple):
    return ">>{}: {}".format(message_tuple[0], message_tuple[1])
