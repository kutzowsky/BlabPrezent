#!/usr/bin/env python
# -*- coding: utf-8 -*-


from nose.tools import *
from ddt import ddt, data, unpack

import messageparser


@ddt
class TestsMessageParser(object):
    @data(
        'user1 > user2: ok :)',
        'user1 >> user2: ok :)'
    )
    def test_when_message_contains_two_or_one_less_than_symbols_in_second_column_is_directed_should_return_true(self, message):
        output = messageparser.is_directed(message)
        assert_true(output)

    def test_when_message_contains_two_less_than_symbols_in_second_column_is_private_directed_should_return_true(self):
        output = messageparser.is_directed_private('user1 >> user2: ok :)')
        assert_true(output)

    @data(
        'user1 > user2: nie ok :(',
        'abc',
        'Bla bla blaaa',
        '',
    )
    def test_when_message_not_contains_two_less_than_symbols_in_second_column_is_private_directed_should_return_false(self, message):
        output = messageparser.is_directed_private(message)
        assert_false(output)

    @data(
        ('user1 > user2: nie ok :(', 'user1'),
        ('user1 >> user2: nie ok :(', 'user1')
    )
    @unpack
    def test_get_sender_from_should_return_sender_from_directed_message(self, message, expected_sender):
        sender = messageparser.get_sender_from(message)
        assert_equal(sender, expected_sender)

    @data(('user1 > user2: ok :) | http://link.to.message', 'ok :)'),
          ('user1 >> user2: nie ok :( | http://link.to.message', 'nie ok :('),
          ('user1 >> user2: : aaaaa ::: bbbb : | http://link.to.message', ': aaaaa ::: bbbb :'),
          ('user1 >> user2: : hello! | http://link.to.message', ': hello!'),
          ('user1 >> user2: ||| hello! | http://link.to.message', '||| hello!')
    )
    @unpack
    def test_get_content_from_should_return_contents_from_directed_message(self, message, expected_content):
        content = messageparser.get_content_from(message)
        assert_equal(content, expected_content)


    def when_message_has_blabprezent_command_has_blabprezent_command_metod_should_return_true(self):
        message = 'someuser >> bot: blabprezent Jan Kowalski, Winogronowa 123/3, Pcim Dolny'

        output = messageparser.has_blabprezent_command(message)

        assert_true(output)

    def when_message_has_blabprezent_command_has_not_blabprezent_command_metod_should_return_false(self):
        message = 'someuser >> bot: Jan Kowalski, Winogronowa 123/3, Pcim Dolny'

        output = messageparser.has_blabprezent_command(message)

        assert_false(output)

    def when_message_has_blabprezent_command_get_user_data_from_method_should_extract_user_data(self):
        message = 'someuser >> bot: blabprezent Jan Kowalski, Winogronowa 123/3, Pcim Dolny'
        expected_user_data = 'Jan Kowalski, Winogronowa 123/3, Pcim Dolny'

        user_data = messageparser.get_user_data_from(message)

        assert_equal(expected_user_data, user_data)