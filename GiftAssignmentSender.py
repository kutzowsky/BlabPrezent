#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from sleekxmpp import ClientXMPP

import configreader
import datamanager
import strings


class GiftAssignmentSender(ClientXMPP):
    def __init__(self, bot_configuration):
        ClientXMPP.__init__(self, bot_configuration.jid, bot_configuration.password)

        self.add_event_handler("session_start", self.on_session_start)

        self.blabler_bot_jid = bot_configuration.blabler_bot_jid

    def on_session_start(self, _):
        self.send_presence()

        gift_assigments = datamanager.get_gift_assignments()

        for gift_assigment in gift_assigments:
            gifter = gift_assigment[0]
            gifted = gift_assigment[1]
            user_address = datamanager.get_address_for(gifted)
            gift_assigment_notification = strings.gift_assigment_notification.format(gifted, user_address)
            message = ">>{}: {}".format(gifter, gift_assigment_notification)
            logging.info('Sending to {} info about {}'.format(gifter, gifted))
            logging.debug(message)
            self.send_message(mto=self.blabler_bot_jid, mbody=message)


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

    bot_configuration = configreader.get_bot_configuration()

    bot = GiftAssignmentSender(bot_configuration)
    bot.connect()
    bot.process(block=False)