#!/usr/bin/env python
# -*- coding: utf-8 -*-


from ddt import ddt, data
from mock import patch
from nose.tools import *

from config import strings
from messaging import messagehandler


@ddt
class TestsMessageHandler():
    def test_handle_should_not_throw(self):
        messagehandler.handle('some message not a massage')

    # TODO: patchowac mesaageparsera zeby testowac tylko i wylacznie handlera
    @data(
        'Konstantynopolitanczykowianeczka',
        'Cztery kuce w stajence. Nogi maja a nie rece.'
    )
    def test_when_message_is_not_directed_handle_should_return_none(self, message):
        answer = messagehandler.handle(message)
        assert_equal(answer, None)

    @data(
        "someuser > bot: Raz dwa trzy, próba mikrofonu!",
        "someuser > bot: dodaj Jan Kowalski, Winogronowa 123/3, Pcim Dolny",
    )
    def test_when_message_is_directed_public_should_return_public_mesage_warn_text(self, message):
        expected_answer = ">>someuser: " + strings.public_message_warn
        answer = messagehandler.handle(message)
        assert_equal(answer, expected_answer)

    @data(
        "someuser >> bot: dodaj Jan Kowalski, Winogronowa 123/3, Pcim Dolny",
        "someuser >> bot: Jan Kowalski, Winogronowa 123/3, Pcim Dolny"
    )
    @patch('commandhandlers.addinghandler.handle_message_content')
    def test_when_message_is_directed_private_should_call_message_content_handler(self, message, handle_message_content):
        messagehandler.handle(message)

        assert_true(handle_message_content.called)

    @patch('commandhandlers.addinghandler.handle_message_content')
    def test_when_message_is_directed_private_should_call_message_content_handler_with_rigt_arguments(self, handle_message_content):
        message = "someuser >> bot: dodaj Jan Kowalski, Winogronowa 123/3, Pcim Dolny"
        expected_handle_message_content_args  = ('someuser', 'dodaj Jan Kowalski, Winogronowa 123/3, Pcim Dolny')

        messagehandler.handle(message)
        args, _ = handle_message_content.call_args

        assert_true(handle_message_content.called)
        assert_equal(args, expected_handle_message_content_args)

    @patch('commandhandlers.addinghandler.handle_message_content')
    def test_when_message_is_directed_private_should_return_output_from_message_content_handler_as_private_message(self, handle_message_content):
        message = "someuser >> bot: dodaj Jan Kowalski, Winogronowa 123/3, Pcim Dolny"
        handle_message_content.return_value = 'Patataj'
        expected_answer = '>>someuser: Patataj'

        answer = messagehandler.handle(message)

        assert_equal(answer, expected_answer)