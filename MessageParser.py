#!/usr/bin/env python
# -*- coding: utf-8 -*-


class MessageParser(object):
    @staticmethod
    def is_private(message):
        return message.split(' ')[1] == '>>'

    @staticmethod
    def get_sender_from(message):
        return message.split(' ')[0]

    @staticmethod
    def get_content_from(message):
        return message[message.index(':') + 2:]
