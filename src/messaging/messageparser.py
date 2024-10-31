#!/usr/bin/env python

def is_directed(message):
    message_splitted = message.split(' ')
    if len(message_splitted) == 1:
        return False
    else:
        return message_splitted[1] == '>' or message_splitted[1] == '>>'


def is_directed_private(message):
    if is_directed(message):
        message_splitted = message.split(' ')
        return message_splitted[1] == '>>'


def is_directed_public(message):
    if is_directed(message):
        message_splitted = message.split(' ')
        return message_splitted[1] == '>'


def get_sender_from(message):
    return message.split(' ')[0]


def get_content_from(message):
    message_without_link = _trim_message_link(message)
    message_without_usernames = _trim_usernames(message_without_link)

    return message_without_usernames


def get_command_from(message):
    return message.split()[0].replace(":", "") if message else None


def remove_command_from(message):
    return ' '.join(message.split()[1:]) if message else None


def _trim_message_link(message):
    return ''.join(message.split(' | ')[:1])


def _trim_usernames(message):
    return message[message.index(':') + 2:]
