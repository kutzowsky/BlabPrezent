#!/usr/bin/env python

import logging

from . import messageparser
from src.commandhandlers import userdatahandler, confirmationshandler
from src.config import strings


class MessageHandler:
    def __init__(self, participant_list_open=True):
        self.logger = logging.getLogger()

        if participant_list_open:
            self.message_content_handler = userdatahandler
        else:
            self.message_content_handler = confirmationshandler

    def handle(self, message):
        if not messageparser.is_directed(message):
            return None

        sender = messageparser.get_sender_from(message)
        answers = None

        if messageparser.is_directed_private(message):
            self.logger.debug('Directed private message: ' + message)

            message_content = messageparser.get_content_from(message)
            answers = self.message_content_handler.handle_message_content(sender, message_content)

        if messageparser.is_directed_public(message):
            self.logger.debug('Directed public message: ' + message)
            self.logger.debug('Sending warning')
            answers = [(sender, strings.public_message_warn)]

        answers_text = map(self._create_private_message_text, answers)
        return answers_text

    @staticmethod
    def _create_private_message_text(message_tuple):
        return ">>{}: {}".format(message_tuple[0], message_tuple[1])
