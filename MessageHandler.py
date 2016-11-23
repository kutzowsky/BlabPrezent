#!/usr/bin/env python
# -*- coding: utf-8 -*-

from MessageParser import MessageParser
from DataManager import DataManager
import Strings

#todo: moduly zamiast klas ze statycznymi metodami
class MessageHandler(object):
    @staticmethod
    def handle(message):
        if not MessageParser.is_directed(message):
            return None

        sender = MessageParser.get_sender_from(message)
        answer = None

        if MessageParser.is_directed_private(message):
            if MessageParser.has_blabprezent_command(message):
                user_data = MessageParser.get_user_data_from(message)

                try:
                    DataManager.save_user_data(sender, user_data)
                except:
                    answer = Strings.error_text
                else:
                    answer = Strings.data_saved
            else:
                answer = Strings.help_text

        if MessageParser.is_directed_public(message):
            answer = Strings.public_message_warn

        return MessageHandler.__create_private_message(sender, answer)

    @staticmethod
    def __create_private_message(recipient, content):
        return u">>{}: {}".format(recipient, content)