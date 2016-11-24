#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from sleekxmpp import ClientXMPP

import messagehandler
import configreader


class Bot(ClientXMPP):
    def __init__(self, bot_configuration):
        ClientXMPP.__init__(self, bot_configuration.jid, bot_configuration.password)

        self.add_event_handler("session_start", self.on_session_start)
        self.add_event_handler("message", self.on_message)

        self.blabler_bot_jid = bot_configuration.blabler_bot_jid

    def on_session_start(self, _):
        self.send_presence()

    def on_message(self, message):
        if message['type'] in ('chat', 'normal') and message["from"] == self.blabler_bot_jid:
            answer = messagehandler.handle(message['body'])
            if answer is not None:
                message.reply(answer).send()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s')

    bot_configuration = configreader.get_bot_configuration()

    bot = Bot(bot_configuration)
    bot.connect()
    bot.process(block=False)