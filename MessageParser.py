#!/usr/bin/env python
# -*- coding: utf-8 -*-


class MessageParser(object):
    @staticmethod
    def is_directed_private(message):
        message_splitted = message.split(' ')
        if len(message_splitted) == 1:
            return False
        else:
            return message_splitted[1] == '>>'

    @staticmethod
    def is_directed_public(message):
        message_splitted = message.split(' ')
        if len(message_splitted) == 1:
            return False
        else:
            return message_splitted[1] == '>'

    @staticmethod
    def get_sender_from(message):
        return message.split(' ')[0]

    @staticmethod
    def get_content_from(message):
        # todo: refactor, bo to magia
        return ''.join(message[message.index(':') + 2:].split(' | ')[:1])
