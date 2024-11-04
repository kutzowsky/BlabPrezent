import pytest

from src.messaging import messageparser


@pytest.mark.parametrize('message', [
    'user1 > user2: ok :)',
    'user1 >> user2: ok :)'
])
def test_when_message_contains_two_or_one_less_than_symbols_in_second_column_is_directed_should_return_true(message):
    output = messageparser.is_directed(message)
    assert output is True


def test_when_message_contains_two_less_than_symbols_in_second_column_is_private_directed_should_return_true():
    output = messageparser.is_directed_private('user1 >> user2: ok :)')
    assert output is True


@pytest.mark.parametrize('message', [
    'user1 > user2: nie ok :(',
    'abc',
    'Bla bla blaaa',
    '',
])
def test_when_message_not_contains_two_less_than_symbols_in_second_column_is_private_directed_should_return_false(message):
    output = messageparser.is_directed_private(message)
    assert bool(output) is False


@pytest.mark.parametrize('message, expected_sender', [
    ('user1 > user2: nie ok :(', 'user1'),
    ('user1 >> user2: nie ok :(', 'user1')
])
def test_get_sender_from_should_return_sender_from_directed_message(message, expected_sender):
    sender = messageparser.get_sender_from(message)
    assert sender == expected_sender


@pytest.mark.parametrize('message, expected_content', [
    ('user1 >> user2: nie ok :( | http://link.to.message', 'nie ok :('),
    ('user1 >> user2: : aaaaa ::: bbbb : | http://link.to.message', ': aaaaa ::: bbbb :'),
    ('user1 >> user2: : hello! | http://link.to.message', ': hello!'),
    ('user1 >> user2: ||| hello! | http://link.to.message', '||| hello!')
])
def test_get_content_from_should_return_contents_from_directed_message(message, expected_content):
    content = messageparser.get_content_from(message)
    assert content == expected_content


def test_when_message_content_is_not_empty_get_command_from_should_return_first_word_from_message_content():
    message_content = 'rule the world!'
    expected_command = 'rule'

    command = messageparser.get_command_from(message_content)

    assert command == expected_command


def test_when_message_content_is_empty_get_command_from_should_return_none():
    message_content = ''

    command = messageparser.get_command_from(message_content)

    assert command is None


def test_when_message_content_is_not_empty_remove_command_from_should_return_message_content_without_first_word():
    message_content = 'rule the world!'
    expected_content = 'the world!'

    content_without_command = messageparser.remove_command_from(message_content)

    assert content_without_command == expected_content


def test_when_message_content_is_empty_remove_command_from_should_return_none():
    message_content = ''

    command = messageparser.remove_command_from(message_content)

    assert command is None
