#!/usr/bin/env python

import logging

from slixmpp import ClientXMPP

from config import settings
from messaging import MessageHandler


class Bot(ClientXMPP):
    def __init__(self, login, password, blabler_bot_jid):
        ClientXMPP.__init__(self, login, password)

        self.add_event_handler("session_start", self.on_session_start)
        self.add_event_handler("message", self.on_message)

        self.blabler_bot_jid = blabler_bot_jid

        self.message_handler = MessageHandler(settings.General.participant_list_open)

    def on_session_start(self, _):
        self.send_presence()

    def on_message(self, message):
        if message['type'] in ('chat', 'normal') and message["from"] == self.blabler_bot_jid:
            answers = self.message_handler.handle(message['body'])
            if answers:
                for answer in answers:
                    message.reply(answer).send()


def _set_logger():
    global logger
    logger = logging.getLogger()
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

    bot = Bot(settings.JabberBot.jid, settings.JabberBot.password, settings.JabberBot.blabler_bot_jid)
    bot.connect()
    bot.process()
