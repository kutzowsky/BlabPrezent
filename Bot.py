#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from sleekxmpp import ClientXMPP

from config import configreader
from messaging import messagehandler


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


def _set_logger():
    global logger
    logger = logging.getLogger()
    mypydupa = 'dupa'
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler('bot.log')
    file_handler.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


if __name__ == '__main__':
    _set_logger()

    logger.info('Started')

    bot_configuration = configreader.get_bot_configuration()

    bot = Bot(bot_configuration)
    bot.connect()
    bot.process(block=False)
