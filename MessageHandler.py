#!/usr/bin/env python
# -*- coding: utf-8 -*-

from MessageParser import MessageParser
from DataManager import DataManager
import Strings

#todo: moduly zamiast klas ze statycznymi metodami
#todo: testy na wykorzystanie DataManagera
class MessageHandler(object):
    @staticmethod
    #todo uporzadkowac
    def handle(message):
        if MessageParser.is_private(message):
            sender = MessageParser.get_sender_from(message)
            message_content = MessageParser.get_content_from(message)
            if message_content.startswith('BLABPREZENT'):
                try:
                    address = message_content.strip('BLABPREZENT ')
                    DataManager.save_user_data(sender, address)
                except:
                    return MessageHandler.__create_private_message(sender, Strings.error_text)

                return MessageHandler.__create_private_message(sender, Strings.data_saved)
            else:
                return MessageHandler.__create_private_message(sender, Strings.help_text)
        else:
            return None

    @staticmethod
    def __create_private_message(recipient, content):
        return u">>{}: {}".format(recipient, content)