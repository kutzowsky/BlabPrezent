#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from sleekxmpp import ClientXMPP

import TestingCredentials


class Bot(ClientXMPP):
    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)

    def session_start(self, event):
        self.send_presence()

    @staticmethod
    def message(msg):
        if msg['type'] in ('chat', 'normal') and msg["from"] == "blabler@blabler.pl":
            pass
            # msg.reply("Thanks for sending\n%(body)s" % msg).send()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s')

    bot = Bot(TestingCredentials.jid, TestingCredentials.password)
    bot.connect()
    bot.process(block=False)