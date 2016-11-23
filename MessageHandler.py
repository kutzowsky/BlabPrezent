#!/usr/bin/env python
# -*- coding: utf-8 -*-

from MessageParser import MessageParser
from DataManager import DataManager
import Strings

#todo: moduly zamiast klas ze statycznymi metodami
class MessageHandler(object):
    @staticmethod
    def handle(message):
        sender = MessageParser.get_sender_from(message)

        if MessageParser.is_directed_private(message):
            message_content = MessageParser.get_content_from(message)

            if message_content.startswith(Strings.blabprezent_command):
                address = message_content.strip(Strings.blabprezent_command + ' ')
                try:
                    DataManager.save_user_data(sender, address)
                except:
                    answer = Strings.error_text
                else:
                    answer = Strings.data_saved
            else:
                answer = Strings.help_text
        else:
            if MessageParser.is_directed_public(message):
                answer = Strings.public_message_warn
            else:
                return None

        return MessageHandler.__create_private_message(sender, answer)

    @staticmethod
    def __create_private_message(recipient, content):
        return u">>{}: {}".format(recipient, content)