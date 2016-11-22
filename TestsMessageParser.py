#!/usr/bin/env python
# -*- coding: utf-8 -*-


from nose.tools import *
from ddt import ddt, data, unpack

from MessageParser import MessageParser


@ddt
class TestsMessageParser(object):
    def test_when_message_contains_two_less_than_symbols_in_second_column_is_private_should_return_true(self):
        output = MessageParser.is_private('user1 >> user2: ok :)')
        assert_true(output)

    @data(
        'user1 > user2: nie ok :(',
        'abc',
        'Bla bla blaaa',
        '',
    )
    def test_when_message_not_contains_two_less_than_symbols_in_second_column_is_private_should_return_false(self, message):
        output = MessageParser.is_private(message)
        assert_false(output)

    @data(
        ('user1 > user2: nie ok :(', 'user1'),
        ('user1 >> user2: nie ok :(', 'user1')
    )
    @unpack
    def test_get_sender_from_should_return_sender_from_directed_message(self, message, expected_sender):
        sender = MessageParser.get_sender_from(message)
        assert_equal(sender, expected_sender)

    @data(('user1 > user2: ok :) | http://link.to.message', 'ok :)'),
          ('user1 >> user2: nie ok :( | http://link.to.message', 'nie ok :('),
          ('user1 >> user2: : aaaaa ::: bbbb : | http://link.to.message', ': aaaaa ::: bbbb :'),
          ('user1 >> user2: : hello! | http://link.to.message', ': hello!'),
          ('user1 >> user2: ||| hello! | http://link.to.message', '||| hello!')
    )
    @unpack
    def test_get_content_from_should_return_contents_from_directed_message(self, message, expected_content):
        content = MessageParser.get_content_from(message)
        assert_equal(content, expected_content)
