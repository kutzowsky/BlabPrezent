#!/usr/bin/env python

import logging
import time

from slixmpp import ClientXMPP

from src.config import settings, strings
from src.dal import datamanager
from src.wwwparsing import BlabWebsiteClient


class GiftAssignmentSender:
    def __init__(self, mode='xmpp'):
        if mode not in ('xmpp', 'www'):
            raise Exception('Unknown mode')

        if mode == 'xmpp':
            self.sender = GiftAssignmentSenderXMPP()
            self.sender.connect()
            self.sender.process()

        if mode == 'www':
            self.sender = GiftAssignmentSenderWWW()

    def send_assignments(self, wait_seconds=2):
        gift_assignments = datamanager.get_gift_assignments()

        for gift_assignment in gift_assignments:
            gift_sender = gift_assignment[0]
            gift_receiver = gift_assignment[1]
            user_address = datamanager.get_address_for(gift_receiver)
            gift_assignment_notification = strings.gift_assignment_notification.format(gift_receiver, user_address)
            message = ">>{}: {}".format(gift_sender, gift_assignment_notification)
            logging.info('Sending to {} info about {}'.format(gift_sender, gift_receiver))
            logging.debug(message)
            self.sender.send_assignment(message)
            time.sleep(wait_seconds)


class GiftAssignmentSenderXMPP(ClientXMPP):
    def __init__(self):
        ClientXMPP.__init__(self, settings.JabberBot.jid, settings.JabberBot.password)

        self.blabler_bot_jid = settings.JabberBot.blabler_bot_jid
        self.add_event_handler("session_start", self.on_session_start)

    def on_session_start(self, _):
        self.send_presence()

    def send_assignment(self, text):
        self.send_message(mto=self.blabler_bot_jid, mbody=text)


class GiftAssignmentSenderWWW:
    def __init__(self, website_client=BlabWebsiteClient()):
        self.website_client = website_client
        self.website_client.login(settings.WebsiteBot.website_login, settings.WebsiteBot.website_password)

    def send_assignment(self, text):
        self.website_client.send_message(text)
