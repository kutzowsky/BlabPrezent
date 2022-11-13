#!/usr/bin/env python

import logging
import time

from slixmpp import ClientXMPP

from config import configreader, strings
from dal import datamanager
from wwwparsing import BlabWebsiteClient


class GiftAssignmentSender:
    def __init__(self, bot_configuration, mode='xmpp'):
        if mode not in ('xmpp', 'www'):
            raise Exception('Unknown mode')

        if mode == 'xmpp':
            self.sender = GiftAssignmentSenderXMPP(bot_configuration)
            self.sender.connect()
            self.sender.process()

        if mode == 'www':
            self.sender = GiftAssignmentSenderWWW(bot_configuration)

    def send_assigments(self, wait_seconds=2):
        gift_assigments = datamanager.get_gift_assignments()

        for gift_assigment in gift_assigments:
            gifter = gift_assigment[0]
            gifted = gift_assigment[1]
            user_address = datamanager.get_address_for(gifted)
            gift_assigment_notification = strings.gift_assigment_notification.format(gifted, user_address)
            message = ">>{}: {}".format(gifter, gift_assigment_notification)
            logging.info('Sending to {} info about {}'.format(gifter, gifted))
            logging.debug(message)
            self.sender.send_assignment(message)
            time.sleep(wait_seconds)


class GiftAssignmentSenderXMPP(ClientXMPP):
    def __init__(self, bot_configuration):
        ClientXMPP.__init__(self, bot_configuration.jid, bot_configuration.password)

        self.blabler_bot_jid = bot_configuration.blabler_bot_jid
        self.add_event_handler("session_start", self.on_session_start)

    def on_session_start(self, _):
        self.send_presence()

    def send_assignment(self, text):
        self.send_message(mto=self.blabler_bot_jid, mbody=text)


class GiftAssignmentSenderWWW:
    def __init__(self, bot_configuration, website_client=BlabWebsiteClient()):
        self.website_client = website_client
        self.website_client.login(bot_configuration.website_login, bot_configuration.website_password)

    def send_assignment(self, text):
        self.website_client.send_message(text)


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

    configuration = configreader.get_bot_configuration()

    sender = GiftAssignmentSender(configuration, mode='www')
    sender.send_assigments()
