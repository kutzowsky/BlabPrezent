#!/usr/bin/env python
# -*- coding: utf-8 -*-


class MessageParser(object):
    _BLABPREZENT_COMMAND = 'blabprezent'

    @staticmethod
    def is_directed(message):
        message_splitted = message.split(' ')
        if len(message_splitted) == 1:
            return False
        else:
            return message_splitted[1] == '>' or message_splitted[1] == '>>'

    @staticmethod
    def is_directed_private(message):
        if MessageParser.is_directed(message):
            message_splitted = message.split(' ')
            return message_splitted[1] == '>>'

    @staticmethod
    def is_directed_public(message):
        if MessageParser.is_directed(message):
            message_splitted = message.split(' ')
            return message_splitted[1] == '>'

    @staticmethod
    def get_sender_from(message):
        return message.split(' ')[0]

    @staticmethod
    def get_content_from(message):
        message_without_link = MessageParser._trim_message_link(message)
        message_without_usernames = MessageParser._trim_usernames(message_without_link)

        return message_without_usernames

    @staticmethod
    def _trim_message_link(message):
        return ''.join(message.split(' | ')[:1])

    @staticmethod
    def _trim_usernames(message):
        return message[message.index(':') + 2:]

    @staticmethod
    def has_blabprezent_command(message):
        message_content = MessageParser.get_content_from(message)
        return message_content.startswith(MessageParser._BLABPREZENT_COMMAND)

    @staticmethod
    def get_user_data_from(message):
        message_content = MessageParser.get_content_from(message)
        return  message_content.strip(MessageParser._BLABPREZENT_COMMAND + ' ')