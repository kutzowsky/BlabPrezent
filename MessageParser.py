#!/usr/bin/env python
# -*- coding: utf-8 -*-


class MessageParser(object):
    @staticmethod
    def is_private(message):
        message_splitted = message.split(' ')
        if len(message_splitted) == 1:
            return False
        else:
            return message_splitted[1] == '>>'

    @staticmethod
    def get_sender_from(message):
        return message.split(' ')[0]

    @staticmethod
    def get_content_from(message):
        return message[message.index(':') + 2:]
