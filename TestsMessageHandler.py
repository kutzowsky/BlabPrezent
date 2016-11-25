#!/usr/bin/env python
# -*- coding: utf-8 -*-


from nose.tools import *
from mock import patch
from ddt import ddt, data

import messagehandler
import strings


@ddt
class TestsMessageHandler(object):
    def test_handle_should_not_throw(self):
        messagehandler.handle('some message not a massage')

    @data(
        'Konstantynopolitanczykowianeczka',
        'Cztery kuce w stajence. Nogi maja a nie rece.'
    )
    def test_when_message_is_not_private_handle_should_return_none(self, message):
        answer = messagehandler.handle(message)
        assert_equal(answer, None)

    def test_when_private_message_content_not_starts_with_add_command_should_return_help_text_private_message(self):
        expected_message = ">>someuser: " + strings.help_text
        answer = messagehandler.handle("someuser >> bot: Don't wanna, don't, wanna don't wanna!")
        assert_equal(answer, expected_message)

    def test_when_private_message_content_starts_with_add_command_should_return_data_saved_text_private_message(self):
        expected_message = ">>someuser: " + strings.data_saved
        answer = messagehandler.handle("someuser >> bot: dodaj Jan Kowalski, Winogronowa 123/3, Pcim Dolny")
        assert_equal(answer, expected_message)

    @data(
        "someuser > bot: Raz dwa trzy, próba mikrofonu!",
        "someuser > bot: dodaj Jan Kowalski, Winogronowa 123/3, Pcim Dolny",
    )
    def test_when_someone_send_public_message_should_return_public_mesage_warn_text(self, message):
        expected_answer = ">>someuser: " + strings.public_message_warn
        answer = messagehandler.handle(message)
        assert_equal(answer, expected_answer)

    @patch('DataManager.DataManager.save_user_data')
    def test_when_private_message_content_starts_with_add_command_should_call_datamanager_save_data(self, save_data):
        message = "someuser >> bot: dodaj Jan Kowalski, Winogronowa 123/3, Pcim Dolny"
        expected_save_data_args = ('someuser', 'Jan Kowalski, Winogronowa 123/3, Pcim Dolny')

        messagehandler.handle(message)

        args, _ = save_data.call_args

        assert_true(save_data.called)
        assert_equal(args, expected_save_data_args)

    @patch('DataManager.DataManager.save_user_data')
    def test_when_saving_data_throws_exception_should_return_error_text(self, save_data):
        message = "someuser >> bot: dodaj Jan Kowalski, Winogronowa 123/3, Pcim Dolny"
        expected_answer = ">>someuser: " + strings.error_text
        save_data.side_effect = Exception

        answer = messagehandler.handle(message)

        assert_true(save_data.called)
        assert_equal(answer, expected_answer)

    @patch('DataManager.DataManager.save_user_data')
    def test_when_private_message_content_not_starts_with_add_command_should_not_call_datamanager_save_data(self, save_data):
        message = "someuser >> bot: O co chodzi?"

        messagehandler.handle(message)

        assert_false(save_data.called)

    @patch('DataManager.DataManager.save_user_data')
    def test_when_message_is_not_directed_should_not_call_datamanager_save_data(self, save_data):
        message = "Tralalalala"

        messagehandler.handle(message)

        assert_false(save_data.called)