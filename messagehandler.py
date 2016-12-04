#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import addinghandler as messagecontenthandler
import messageparser
import strings

logger = logging.getLogger()


def handle(message):
    if not messageparser.is_directed(message):
        return None

    sender = messageparser.get_sender_from(message)
    answer = None

    if messageparser.is_directed_private(message):
        logger.info('Directed private message: ' + message)

        message_content = messageparser.get_content_from(message)
        answer = messagecontenthandler.handle_message_content(sender, message_content)

    if messageparser.is_directed_public(message):
        logger.debug('Directed public message: ' + message)
        logger.debug('Sending warning')
        answer = strings.public_message_warn

    return _create_private_message(sender, answer)


def _create_private_message(recipient, content):
    return u">>{}: {}".format(recipient, content)