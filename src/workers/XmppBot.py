#!/usr/bin/env python

from slixmpp import ClientXMPP

from src.config import settings
from src.messaging import MessageHandler


class XmppBot(ClientXMPP):
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
