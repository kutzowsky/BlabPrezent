#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from sqlite3 import IntegrityError

from ddt import ddt, data
from freezegun import freeze_time
from mock import patch
from nose.tools import *

from commandhandlers import confirmationshandler
from config import strings


@ddt
class TestsConfirmationsHandler():
    def test_handle_message_content_should_not_throw(self):
        confirmationshandler.handle_message_content('user', 'content')

    def test_when_message_has_unknown_command_should_return_help_text(self):
        answer = confirmationshandler.handle_message_content('user', 'djinfdushfdushfcvuidhfuhv')

        assert_equal(answer, strings.help_text)

    @patch('dal.datamanager.save_send_confirmation')
    @patch('dal.datamanager.save_received_confirmation')
    def test_when_message_has_unknown_command_should_not_try_to_save_any_confirmation(self, save_send_confirmation, save_received_confirmation):
        confirmationshandler.handle_message_content('user', 'Tralalalala')

        assert_false(save_send_confirmation.called)
        assert_false(save_received_confirmation.called)

    def test_when_message_has_add_command_should_return_data_gathering_disabled_text(self):
        answer = confirmationshandler.handle_message_content('user', 'dodaj adres')

        assert_equal(answer, strings.data_gathering_disabled)

    @patch('dal.datamanager.save_send_confirmation')
    @patch('dal.datamanager.save_received_confirmation')
    def test_when_message_has_add_command_should_not_try_to_save_any_confirmation(self, save_send_confirmation, save_received_confirmation):
        confirmationshandler.handle_message_content('user', 'dodaj adres')

        assert_false(save_send_confirmation.called)
        assert_false(save_received_confirmation.called)

    @data(
        'wyslano',
        'wysłano',
    )
    @patch('dal.datamanager.get_participants')
    @patch('dal.datamanager.save_send_confirmation')
    @freeze_time("2012-01-14 12:12")
    def test_when_message_has_sent_command_should_save_send_confirmation(self, message, save_send_confirmation, get_participants):
        user = 'someuser'
        expected_args = (user, datetime.datetime(2012, 1, 14, 12, 12))
        get_participants.return_value = [user]

        confirmationshandler.handle_message_content(user, message)
        args, _ = save_send_confirmation.call_args

        assert_true(save_send_confirmation.called)
        assert_equals(args, expected_args)

    @data(
        'wyslano',
        'wysłano'
    )
    @patch('dal.datamanager.get_participants')
    @patch('dal.datamanager.save_send_confirmation')
    def test_when_successfully_saved_sent_confirmation_should_return_sent_confirmation_saved_test(self, message, save_send_confirmation, get_participants):
        user = 'someuser'
        get_participants.return_value = [user]

        answer = confirmationshandler.handle_message_content(user, message)

        assert_equal(answer, strings.sent_confirmation_saved)

    @data(
        'wyslano',
        'wysłano',
    )
    @patch('dal.datamanager.get_participants')
    @patch('dal.datamanager.save_send_confirmation')
    def test_when_saving_duplicated_confirmation_should_return_confirmation_already_exists_text(self, message, save_send_confirmation, get_participants):
        user = 'someuser'
        save_send_confirmation.side_effect = IntegrityError
        get_participants.return_value = [user]

        answer = confirmationshandler.handle_message_content(user, message)

        assert_equal(answer, strings.confirmation_already_exists)

    @data(
        'wyslano',
        'wysłano',
    )
    @patch('dal.datamanager.save_send_confirmation')
    @patch('dal.datamanager.get_participants')
    def test_when_there_is_error_on_saving_sent_confirmation_should_return_error_text(self, message, save_send_confirmation, get_participants):
        user = 'someuser'
        save_send_confirmation.side_effect = Exception

        answer = confirmationshandler.handle_message_content(user, message)

        assert_equal(answer, strings.error_text)

    @patch('dal.datamanager.get_participants')
    @patch('dal.datamanager.save_received_confirmation')
    @freeze_time("2012-01-14 12:12")
    def test_when_message_has_received_command_should_save_received_confirmation(self, save_received_confirmation, get_participants):
        user = 'someuser'
        message = 'otrzymano'
        expected_args = (user, datetime.datetime(2012, 1, 14, 12, 12))
        get_participants.return_value = [user]

        confirmationshandler.handle_message_content(user, message)
        args, _ = save_received_confirmation.call_args

        assert_true(save_received_confirmation.called)
        assert_equals(args, expected_args)

    @patch('dal.datamanager.get_participants')
    @patch('dal.datamanager.save_received_confirmation')
    def test_when_successfully_saved_received_confirmation_should_return_received_confirmation_saved_test(self, save_received_confirmation, get_participants):
        user = 'someuser'
        message = 'otrzymano'
        get_participants.return_value = [user]

        answer = confirmationshandler.handle_message_content(user, message)

        assert_equal(answer, strings.received_confirmation_saved)

    @patch('dal.datamanager.get_participants')
    @patch('dal.datamanager.save_received_confirmation')
    def test_when_saving_duplicated_confirmation_should_return_confirmation_already_exists_text(self, save_received_confirmation, get_participants):
        user = 'someuser'
        message = 'otrzymano'
        save_received_confirmation.side_effect = IntegrityError
        get_participants.return_value = [user]

        answer = confirmationshandler.handle_message_content(user, message)

        assert_equal(answer, strings.confirmation_already_exists)

    @patch('dal.datamanager.save_received_confirmation')
    @patch('dal.datamanager.get_participants')
    def test_when_there_is_error_on_saving_received_confirmation_should_return_error_text(self, save_received_confirmation, get_participants):
        user = 'someuser'
        message = 'otrzymano'
        save_received_confirmation.side_effect = Exception

        answer = confirmationshandler.handle_message_content(user, message)

        assert_equal(answer, strings.error_text)

    @data(
        'otrzymano',
        'wyslano',
    )
    @patch('dal.datamanager.get_participants')
    @patch('dal.datamanager.save_received_confirmation')
    def test_when_got_confirmation_from_user_not_in_paritipants_list_should_return_not_a_participant_text(self, message, save_received_confirmation, get_participants):
        user = 'someuser'
        get_participants.return_value = ['otherUser', 'alsoOtherUser', 'differentUserAsWell']

        answer = confirmationshandler.handle_message_content(user, message)

        assert_equal(answer, strings.not_a_participant)

    @data(
        'Wyslano',
        'wysłano',
        'Wyslano',
        'wysłaNO',
        'OTRZYMANO',
        'otrzymano',
    )
    @patch('dal.datamanager.save_send_confirmation')
    @patch('dal.datamanager.save_received_confirmation')
    @patch('dal.datamanager.get_participants')
    def test_when_command_has_different_letter_case_should_also_recognize_it(self, message, save_send_confirmation, save_received_confirmation, get_participants):
        user = 'someuser'

        answer = confirmationshandler.handle_message_content(user, message)

        assert_not_equal(answer, strings.help_text)
