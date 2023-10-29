import pytest

import datetime
from sqlite3 import IntegrityError

from commandhandlers import confirmationshandler
from config import strings


def test_handle_message_content_should_not_throw():
    confirmationshandler.handle_message_content('user', 'content')


def test_when_message_has_unknown_command_should_return_help_text():
    user = 'someuser'
    expected_answer = [(user, strings.help_text)]

    answer = confirmationshandler.handle_message_content(user, 'djinfdushfdushfcvuidhfuhv')

    assert answer == expected_answer


def test_when_message_has_unknown_command_should_not_try_to_save_any_confirmation(mocker):
    confirmationshandler.handle_message_content('user', 'Tralalalala')
    save_send_confirmation_mock = mocker.patch('dal.datamanager.save_send_confirmation')
    save_received_confirmation_mock = mocker.patch('dal.datamanager.save_received_confirmation')

    save_send_confirmation_mock.assert_not_called()
    save_received_confirmation_mock.assert_not_called()


def test_when_message_has_add_command_should_return_data_gathering_disabled_text():
    user = 'someuser'
    expected_answer = [(user, strings.data_gathering_disabled)]

    answer = confirmationshandler.handle_message_content(user, 'dodaj adres')

    assert answer == expected_answer


def test_when_message_has_add_command_should_not_try_to_save_any_confirmation(mocker):
    save_send_confirmation_mock = mocker.patch('dal.datamanager.save_send_confirmation')
    save_received_confirmation_mock = mocker.patch('dal.datamanager.save_received_confirmation')

    confirmationshandler.handle_message_content('user', 'dodaj adres')

    save_send_confirmation_mock.assert_not_called()
    save_received_confirmation_mock.assert_not_called()


@pytest.mark.parametrize('message', [
    'wyslano',
    'wysłano',
])
@pytest.mark.freeze_time('2012-01-14 12:12')
def test_when_message_has_sent_command_should_save_send_confirmation(message, mocker):
    user = 'someuser'
    expected_datetime = datetime.datetime(2012, 1, 14, 12, 12)

    get_participants_mock = mocker.patch('dal.datamanager.get_participants')
    mocker.patch('dal.datamanager.get_gift_receiver_from')
    get_participants_mock.return_value = [user]

    save_send_confirmation_mock = mocker.patch('dal.datamanager.save_send_confirmation')

    confirmationshandler.handle_message_content(user, message)

    save_send_confirmation_mock.assert_called_once_with(user, expected_datetime)


@pytest.mark.parametrize('message', [
    'wyslano',
    'wysłano',
])
def test_when_successfully_saved_sent_confirmation_should_return_confirmation_text_and_notification(message, mocker):
    user = 'someuser'
    gift_receiver = 'gift_receiver'
    expected_answer = [
        (user, strings.sent_confirmation_saved),
        (gift_receiver, strings.package_sent_notification)
    ]
    get_participants_mock = mocker.patch('dal.datamanager.get_participants')
    get_participants_mock.return_value = [user]
    mocker.patch('dal.datamanager.save_send_confirmation')
    gift_receiver_from_mock = mocker.patch('dal.datamanager.get_gift_receiver_from')
    gift_receiver_from_mock.return_value = gift_receiver

    answer = confirmationshandler.handle_message_content(user, message)

    assert answer == expected_answer


@pytest.mark.parametrize('message', [
    'wyslano',
    'wysłano',
])
def test_when_saving_duplicated_send_confirmation_should_return_confirmation_already_exists_text(message, mocker):
    user = 'someuser'
    expected_answer = [(user, strings.confirmation_already_exists)]
    save_send_confirmation_mock = mocker.patch('dal.datamanager.save_send_confirmation')
    save_send_confirmation_mock.side_effect = IntegrityError
    get_participants_mock = mocker.patch('dal.datamanager.get_participants')
    get_participants_mock.return_value = [user]

    answer = confirmationshandler.handle_message_content(user, message)

    assert answer == expected_answer


@pytest.mark.parametrize('message', [
    'wyslano',
    'wysłano',
])
def test_when_there_is_error_on_saving_sent_confirmation_should_return_error_text(message, mocker):
    user = 'someuser'
    expected_answer = [(user, strings.error_text)]
    save_send_confirmation_mock = mocker.patch('dal.datamanager.save_send_confirmation')
    save_send_confirmation_mock.side_effect = Exception
    get_participants_mock = mocker.patch('dal.datamanager.get_participants')
    get_participants_mock.return_value = [user]

    answer = confirmationshandler.handle_message_content(user, message)

    assert answer == expected_answer

@pytest.mark.freeze_time('2012-01-14 12:12')
def test_when_message_has_received_command_should_save_received_confirmation(mocker):
    user = 'someuser'
    message = 'otrzymano'
    expected_datetime = datetime.datetime(2012, 1, 14, 12, 12)
    get_participants_mock = mocker.patch('dal.datamanager.get_participants')
    get_participants_mock.return_value = [user]
    mocker.patch('dal.datamanager.get_gift_sender_for')
    save_received_confirmation_mock = mocker.patch('dal.datamanager.save_received_confirmation')

    confirmationshandler.handle_message_content(user, message)

    save_received_confirmation_mock.assert_called_once_with(user, expected_datetime)


def test_when_successfully_saved_received_confirmation_should_return_confirmation_text_and_notification(mocker):
    user = 'someuser'
    gift_sender = 'gift_sender'
    message = 'otrzymano'
    get_participants_mock = mocker.patch('dal.datamanager.get_participants')
    get_participants_mock.return_value = [user]
    get_gift_sender_for_mock = mocker.patch('dal.datamanager.get_gift_sender_for')
    get_gift_sender_for_mock.return_value = gift_sender
    expected_answer = [
        (user, strings.received_confirmation_saved),
        (gift_sender, strings.package_received_notificaton)
    ]
    mocker.patch('dal.datamanager.save_received_confirmation')

    answer = confirmationshandler.handle_message_content(user, message)

    assert answer == expected_answer


def test_when_saving_duplicated_received_confirmation_should_return_confirmation_already_exists_text(mocker):
    user = 'someuser'
    message = 'otrzymano'
    expected_answer = [(user, strings.confirmation_already_exists)]
    save_received_confirmation_mock = mocker.patch('dal.datamanager.save_received_confirmation')
    save_received_confirmation_mock.side_effect = IntegrityError
    get_participants_mock = mocker.patch('dal.datamanager.get_participants')
    get_participants_mock.return_value = [user]

    answer = confirmationshandler.handle_message_content(user, message)

    assert answer == expected_answer


def test_when_there_is_error_on_saving_received_confirmation_should_return_error_text(mocker):
    user = 'someuser'
    message = 'otrzymano'
    expected_answer = [(user, strings.error_text)]
    save_received_confirmation_mock = mocker.patch('dal.datamanager.save_received_confirmation')
    save_received_confirmation_mock.side_effect = Exception
    get_participants_mock = mocker.patch('dal.datamanager.get_participants')
    get_participants_mock.return_value = [user]

    answer = confirmationshandler.handle_message_content(user, message)

    assert answer == expected_answer


@pytest.mark.parametrize('message', [
    'wyslano',
    'wysłano',
])
def test_when_got_confirmation_from_user_not_in_participants_list_should_return_not_a_participant_text(message, mocker):
    user = 'someuser'
    expected_answer = [(user, strings.not_a_participant)]
    get_participants_mock = mocker.patch('dal.datamanager.get_participants')
    get_participants_mock.return_value = ['otherUser', 'alsoOtherUser', 'differentUserAsWell']

    answer = confirmationshandler.handle_message_content(user, message)

    assert answer == expected_answer


@pytest.mark.parametrize('message', [
    'Wyslano',
    'wysłano',
    'Wyslano',
    'wysłaNO',
    'OTRZYMANO',
    'otrzymano',
])
def test_when_command_has_different_letter_case_should_also_recognize_it(message, mocker):
    user = 'someuser'
    mocker.patch('dal.datamanager.save_send_confirmation')
    mocker.patch('dal.datamanager.save_received_confirmation')
    mocker.patch('dal.datamanager.get_participants')

    answer = confirmationshandler.handle_message_content(user, message)

    assert answer != strings.help_text
