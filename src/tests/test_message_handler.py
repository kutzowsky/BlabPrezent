import pytest

from config import strings
from messaging import messagehandler


def test_handle_should_not_throw():
    messagehandler.handle('some message not a massage')


# TODO: patchowac messageparsera zeby testowac tylko i wylacznie handlera
@pytest.mark.parametrize("message", [
    'Konstantynopolitanczykowianeczka',
    'Cztery kuce w stajence. Nogi maja a nie rece.'
])
def test_when_message_is_not_directed_handle_should_return_none(message):
    answer = messagehandler.handle(message)
    assert answer is None


@pytest.mark.parametrize("message", [
    'someuser > bot: Raz dwa trzy, próba mikrofonu!',
    'someuser > bot: dodaj Jan Kowalski, Winogronowa 123/3, Pcim Dolny',
])
def test_when_message_is_directed_public_should_return_public_message_warn_text(message):
    expected_answer = ['>>someuser: ' + strings.public_message_warn]
    answer = messagehandler.handle(message)
    assert list(answer) == expected_answer


@pytest.mark.parametrize('message', [
    'someuser >> bot: dodaj Jan Kowalski, Winogronowa 123/3, Pcim Dolny',
    'someuser >> bot: Jan Kowalski, Winogronowa 123/3, Pcim Dolny'
])
def test_when_message_is_directed_private_should_call_message_content_handler(message, mocker):

    handle_message_content_mock = mocker.patch('commandhandlers.addinghandler.handle_message_content')

    messagehandler.handle(message)

    handle_message_content_mock.assert_called_once()


def test_when_message_is_directed_private_should_call_message_content_handler_with_right_arguments(mocker):
    username = 'someuser'
    message_text = 'dodaj Jan Kowalski, Winogronowa 123/3, Pcim Dolny'
    raw_message = f'{username} >> bot: {message_text}'
    handle_message_content_mock = mocker.patch('commandhandlers.addinghandler.handle_message_content')

    messagehandler.handle(raw_message)

    handle_message_content_mock.assert_called_once_with(username, message_text)


def test_when_message_is_directed_private_should_return_output_from_message_content_handler_as_private_message(mocker):
    user = 'someuser'
    raw_message = f'{user} >> bot: dodaj Jan Kowalski, Winogronowa 123/3, Pcim Dolny'
    handle_message_content_mock = mocker.patch('commandhandlers.addinghandler.handle_message_content')
    handle_message_content_mock.return_value = [(user, 'Patataj')]
    expected_answer = ['>>someuser: Patataj']

    answer = messagehandler.handle(raw_message)

    assert list(answer) == expected_answer
