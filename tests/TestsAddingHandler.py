#!/usr/bin/env python
# -*- coding: utf-8 -*-


from mock import patch
from nose.tools import *
from ddt import ddt, data

from commandhandlers import addinghandler
from config import strings


@ddt
class TestsAddingHandler():
    def test_handle_message_content_should_not_throw(self):
        addinghandler.handle_message_content('user', 'content')

    def test_when_message_has_no_add_command_should_return_help_text(self):
        answer = addinghandler.handle_message_content('user', 'nie dodawaj, odejmuj!')

        assert_equal(answer, strings.help_text)

    @patch('dal.datamanager.save_user_data')
    def test_when_message_has_no_add_command_should_not_try_to_save_data(self, save_user_data):
        addinghandler.handle_message_content('user', 'nie dodawaj, odejmuj!')

        assert_false(save_user_data.called)

    @patch('dal.datamanager.save_user_data')
    def test_when_message_has_add_command_should_try_to_save_data(self, save_user_data):
        user = 'anna'
        message = 'dodaj Anna Maria Smutna 22-111 Ma twarz'
        expected_save_user_data_args = (user, 'Anna Maria Smutna 22-111 Ma twarz')

        addinghandler.handle_message_content(user, message)
        args, _ = save_user_data.call_args

        assert_true(save_user_data.called)
        assert_equal(args, expected_save_user_data_args)

    @patch('dal.datamanager.save_user_data')
    def test_when_successfully_saved_user_data_should_return_data_saved_text(self, save_user_data):
        answer = addinghandler.handle_message_content('user', 'dodaj mnie!')

        assert_equal(answer, strings.data_saved)

    @patch('dal.datamanager.save_user_data')
    def test_when_there_is_error_with_saving_user_data_should_return_error_text(self, save_user_data):
        save_user_data.side_effect = Exception

        answer = addinghandler.handle_message_content('user', 'dodaj mnie!')

        assert_equal(answer, strings.error_text)

    @data(
        'DODAJ',
        'DoDaj',
        'dodaj',
        'Dodaj',
    )
    @patch('dal.datamanager.save_user_data')
    def test_when_command_has_different_letter_case_should_also_recognize_it(self, message, save_user_data):
        user = 'someuser'

        answer = addinghandler.handle_message_content(user, message)

        assert_not_equal(answer, strings.help_text)
