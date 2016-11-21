#!/usr/bin/env python
# -*- coding: utf-8 -*-

from MessageParser import MessageParser
import Strings


class MessageHandler(object):
    @staticmethod
    def handle(message):
        if MessageParser.is_private(message):
            sender = MessageParser.get_sender_from(message)
            message_content = MessageParser.get_content_from(message)
            if message_content.startswith('BLABPREZENT'):
                return MessageHandler.__create_private_message(sender, Strings.data_saved)
            else:
                return MessageHandler.__create_private_message(sender, Strings.help_text)
        else:
            return None

    @staticmethod
    def __create_private_message(recipient, content):
        return u">>{}: {}".format(recipient, content)