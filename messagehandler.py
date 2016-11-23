#!/usr/bin/env python
# -*- coding: utf-8 -*-

import messageparser
import datamanager
import strings


def handle(message):
    if not messageparser.is_directed(message):
        return None

    sender = messageparser.get_sender_from(message)
    answer = None

    if messageparser.is_directed_private(message):
        if messageparser.has_blabprezent_command(message):
            user_data = messageparser.get_user_data_from(message)

            try:
                datamanager.save_user_data(sender, user_data)
            except:
                answer = strings.error_text
            else:
                answer = strings.data_saved
        else:
            answer = strings.help_text

    if messageparser.is_directed_public(message):
        answer = strings.public_message_warn

    return _create_private_message(sender, answer)


def _create_private_message(recipient, content):
    return u">>{}: {}".format(recipient, content)