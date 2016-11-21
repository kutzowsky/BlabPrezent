#!/usr/bin/env python
# -*- coding: utf-8 -*-


from nose.tools import *
from ddt import ddt, data, unpack

from MessageHandler import MessageHandler
import Strings


@ddt
class TestsMessageHandler(object):
    def test_handle_should_not_throw(self):
        MessageHandler.handle('some message not a massage')

    @data(
        'Konstantynopolitanczykowianeczka',
        'Cztery kuce w stajence. Nogi maja a nie rece.'
        'lookash > seksiLejde: hey poklikash?'
    )
    def test_when_message_is_not_private_handle_should_return_none(self, message):
        answer = MessageHandler.handle(message)
        assert_equal(answer, None)

    def test_when_private_message_content_not_starts_with_blabprezent_string_should_return_help_text_private_message(self):
        expected_message = ">>someuser: " + Strings.help_text
        answer = MessageHandler.handle("someuser >> bot: Don't wanna, don't, wanna don't wanna!")
        assert_equal(answer, expected_message)

    def test_when_private_message_content_starts_with_blabprezent_string_should_return_data_saved_text_private_message(self):
        expected_message = ">>someuser: " + Strings.data_saved
        answer = MessageHandler.handle("someuser >> bot: BLABPREZENT Jan Kowalski, Winogronowa 123/3, Pcim Dolny")
        assert_equal(answer, expected_message)