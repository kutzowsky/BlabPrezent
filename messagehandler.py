#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import messageparser
import datamanager
import strings

logger = logging.getLogger()


def handle(message):
    if not messageparser.is_directed(message):
        return None

    sender = messageparser.get_sender_from(message)
    answer = None

    if messageparser.is_directed_private(message):
        logger.info('Directed private message: ' + message)

        if messageparser.has_add_command(message):
            logger.info('Got add command')
            user_data = messageparser.get_user_data_from(message)

            try:
                logger.info('Trying save data for user: ' + sender)
                datamanager.save_user_data(sender, user_data)
            except Exception as exc:
                logger.warn('Data saving failed. Reason: ' + str(exc))
                answer = strings.error_text
            else:
                logger.info('User data saved')
                answer = strings.data_saved
        else:
            logger.info('No command in message')
            answer = strings.help_text

    if messageparser.is_directed_public(message):
        logger.debug('Directed public message: ' + message)
        logger.debug('Sending warning')
        answer = strings.public_message_warn

    return _create_private_message(sender, answer)


def _create_private_message(recipient, content):
    return u">>{}: {}".format(recipient, content)