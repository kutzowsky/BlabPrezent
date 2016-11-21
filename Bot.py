#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from sleekxmpp import ClientXMPP

from MessageHandler import MessageHandler
import TestingCredentials


class Bot(ClientXMPP):
    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)

        self.add_event_handler("session_start", self.on_session_start)
        self.add_event_handler("message", self.on_message)

    def on_session_start(self, _):
        self.send_presence()

    @staticmethod
    def on_message(message):
        if message['type'] in ('chat', 'normal') and message["from"] == TestingCredentials.whitelisted_sender:
            answer = MessageHandler.handle(message['body'])
            if answer is not None:
                message.reply(answer).send()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s')

    bot = Bot(TestingCredentials.jid, TestingCredentials.password)
    bot.connect()
    bot.process(block=False)