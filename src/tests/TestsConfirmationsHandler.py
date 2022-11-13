#!/usr/bin/env python

import datetime
from sqlite3 import IntegrityError

from ddt import ddt, data
from freezegun import freeze_time
from mock import patch
from nose.tools import *

from commandhandlers import confirmationshandler
from config import strings


@ddt
class TestsConfirmationsHandler:
    def test_handle_message_content_should_not_throw(self):
        confirmationshandler.handle_message_content('user', 'content')

    def test_when_message_has_unknown_command_should_return_help_text(self):
        user = 'someuser'
        expected_answer = [(user, strings.help_text)]

        answer = confirmationshandler.handle_message_content(user, 'djinfdushfdushfcvuidhfuhv')

        assert_equal(answer, expected_answer)

    @patch('dal.datamanager.save_send_confirmation')
    @patch('dal.datamanager.save_received_confirmation')
    def test_when_message_has_unknown_command_should_not_try_to_save_any_confirmation(self, save_send_confirmation, save_received_confirmation):
        confirmationshandler.handle_message_content('user', 'Tralalalala')

        assert_false(save_send_confirmation.called)
        assert_false(save_received_confirmation.called)

    def test_when_message_has_add_command_should_return_data_gathering_disabled_text(self):
        user = 'someuser'
        expected_answer = [(user, strings.data_gathering_disabled)]

        answer = confirmationshandler.handle_message_content(user, 'dodaj adres')

        assert_equal(answer, expected_answer)

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
    @patch('dal.datamanager.get_gift_receiver_from')
    @freeze_time("2012-01-14 12:12")
    def test_when_message_has_sent_command_should_save_send_confirmation(self, message, get_gift_receiver_from, save_send_confirmation, get_participants):
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
    @patch('dal.datamanager.get_gift_receiver_from')
    def test_when_successfully_saved_sent_confirmation_should_return_confirmation_text_and_notification(self, message, gift_receiver_from, save_send_confirmation, get_participants):
        user = 'someuser'
        gift_receiver = 'gift_receiver'
        expected_answer = [
            (user, strings.sent_confirmation_saved),
            (gift_receiver, strings.package_sent_notification)
        ]
        get_participants.return_value = [user]
        gift_receiver_from.return_value = gift_receiver

        answer = confirmationshandler.handle_message_content(user, message)

        assert_equal(answer, expected_answer)

    @data(
        'wyslano',
        'wysłano',
    )
    @patch('dal.datamanager.get_participants')
    @patch('dal.datamanager.save_send_confirmation')
    def test_when_saving_duplicated_confirmation_should_return_confirmation_already_exists_text(self, message, save_send_confirmation, get_participants):
        user = 'someuser'
        expected_answer = [(user, strings.confirmation_already_exists)]
        save_send_confirmation.side_effect = IntegrityError
        get_participants.return_value = [user]

        answer = confirmationshandler.handle_message_content(user, message)

        assert_equal(answer, expected_answer)

    @data(
        'wyslano',
        'wysłano',
    )
    @patch('dal.datamanager.save_send_confirmation')
    @patch('dal.datamanager.get_participants')
    def test_when_there_is_error_on_saving_sent_confirmation_should_return_error_text(self, message, save_send_confirmation, get_participants):
        user = 'someuser'
        expected_answer = [(user, strings.error_text)]
        save_send_confirmation.side_effect = Exception

        answer = confirmationshandler.handle_message_content(user, message)

        assert_equal(answer, expected_answer)

    @patch('dal.datamanager.get_participants')
    @patch('dal.datamanager.save_received_confirmation')
    @patch('dal.datamanager.get_gift_sender_for')
    @freeze_time("2012-01-14 12:12")
    def test_when_message_has_received_command_should_save_received_confirmation(self, get_gift_sender_for, save_received_confirmation, get_participants):
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
    @patch('dal.datamanager.get_gift_sender_for')
    def test_when_successfully_saved_received_confirmation_should_return_confirmation_text_and_notification(self, get_gift_sender_for, save_received_confirmation, get_participants):
        user = 'someuser'
        gift_sender = 'gift_sender'
        message = 'otrzymano'
        get_participants.return_value = [user]
        get_gift_sender_for.return_value = gift_sender
        expected_answer = [
            (user, strings.received_confirmation_saved),
            (gift_sender, strings.package_received_notificaton)
        ]

        answer = confirmationshandler.handle_message_content(user, message)

        assert_equal(answer, expected_answer)

    @patch('dal.datamanager.get_participants')
    @patch('dal.datamanager.save_received_confirmation')
    def test_when_saving_duplicated_confirmation_should_return_confirmation_already_exists_text(self, save_received_confirmation, get_participants):
        user = 'someuser'
        message = 'otrzymano'
        expected_answer = [(user, strings.confirmation_already_exists)]
        save_received_confirmation.side_effect = IntegrityError
        get_participants.return_value = [user]

        answer = confirmationshandler.handle_message_content(user, message)

        assert_equal(answer, expected_answer)

    @patch('dal.datamanager.save_received_confirmation')
    @patch('dal.datamanager.get_participants')
    def test_when_there_is_error_on_saving_received_confirmation_should_return_error_text(self, save_received_confirmation, get_participants):
        user = 'someuser'
        message = 'otrzymano'
        expected_answer = [(user, strings.error_text)]
        save_received_confirmation.side_effect = Exception

        answer = confirmationshandler.handle_message_content(user, message)

        assert_equal(answer, expected_answer)

    @data(
        'otrzymano',
        'wyslano',
    )
    @patch('dal.datamanager.get_participants')
    @patch('dal.datamanager.save_received_confirmation')
    def test_when_got_confirmation_from_user_not_in_paritipants_list_should_return_not_a_participant_text(self, message, save_received_confirmation, get_participants):
        user = 'someuser'
        expected_answer = [(user, strings.not_a_participant)]
        get_participants.return_value = ['otherUser', 'alsoOtherUser', 'differentUserAsWell']

        answer = confirmationshandler.handle_message_content(user, message)

        assert_equal(answer, expected_answer)

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
