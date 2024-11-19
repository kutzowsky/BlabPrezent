import pytest

import datetime
from sqlite3 import IntegrityError

from src.commandhandlers import confirmationshandler
from src.config import strings


def test_handle_message_content_should_not_throw():
    confirmationshandler.handle_message_content('user', 'content')


def test_when_message_has_unknown_command_should_return_help_text():
    user = 'someuser'
    expected_answer = [(user, strings.help_text)]

    answer = confirmationshandler.handle_message_content(user, 'djinfdushfdushfcvuidhfuhv')

    assert answer == expected_answer


def test_when_message_has_unknown_command_should_not_try_to_save_any_confirmation(mocker):
    confirmationshandler.handle_message_content('user', 'Tralalalala')
    save_send_confirmation_mock = mocker.patch('src.dal.datamanager.save_send_confirmation')
    save_received_confirmation_mock = mocker.patch('src.dal.datamanager.save_received_confirmation')

    save_send_confirmation_mock.assert_not_called()
    save_received_confirmation_mock.assert_not_called()


def test_when_message_has_add_command_should_return_data_gathering_disabled_text():
    user = 'someuser'
    expected_answer = [(user, strings.data_gathering_disabled)]

    answer = confirmationshandler.handle_message_content(user, 'dodaj adres')

    assert answer == expected_answer


def test_when_message_has_add_command_should_not_try_to_save_any_confirmation(mocker):
    save_send_confirmation_mock = mocker.patch('src.dal.datamanager.save_send_confirmation')
    save_received_confirmation_mock = mocker.patch('src.dal.datamanager.save_received_confirmation')

    confirmationshandler.handle_message_content('user', 'dodaj adres')

    save_send_confirmation_mock.assert_not_called()
    save_received_confirmation_mock.assert_not_called()


def test_when_message_has_delete_command_should_return_data_gathering_disabled_text():
    user = 'someuser'
    expected_answer = [(user, strings.data_gathering_disabled)]

    answer = confirmationshandler.handle_message_content(user, 'usuń')

    assert answer == expected_answer


def test_when_message_has_delete_command_should_not_try_to_delete_user(mocker):
    delete_user_data_mock = mocker.patch('src.dal.datamanager.delete_user_data')

    confirmationshandler.handle_message_content('user', 'usuń')

    delete_user_data_mock.assert_not_called()


@pytest.mark.parametrize('message', [
    'usuń',
    'usun',
    'USUŃ',
    'USUN',
    'Usuń',
    'usun:'
])
def test_when_delete_command_synonym_was_provided_should_also_recognize_it(message, mocker):
    user = 'someuser'
    delete_user_data_mock = mocker.patch('src.dal.datamanager.delete_user_data')

    confirmationshandler.handle_message_content(user, message)

    delete_user_data_mock.assert_not_called()


@pytest.mark.parametrize('message', [
    'wyslano',
    'wysłano',
])
@pytest.mark.freeze_time('2012-01-14 12:12')
def test_when_message_has_sent_command_should_save_send_confirmation(message, mocker):
    user = 'someuser'
    expected_datetime = datetime.datetime(2012, 1, 14, 12, 12)

    is_participant_mock = mocker.patch('src.dal.datamanager.is_participant')
    is_participant_mock.return_value = True
    mocker.patch('src.dal.datamanager.get_gift_receiver_from')

    save_send_confirmation_mock = mocker.patch('src.dal.datamanager.save_send_confirmation')

    confirmationshandler.handle_message_content(user, message)

    save_send_confirmation_mock.assert_called_once_with(user, expected_datetime, None)


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
    is_participant_mock = mocker.patch('src.dal.datamanager.is_participant')
    is_participant_mock.return_value = True
    mocker.patch('src.dal.datamanager.save_send_confirmation')
    gift_receiver_from_mock = mocker.patch('src.dal.datamanager.get_gift_receiver_from')
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
    save_send_confirmation_mock = mocker.patch('src.dal.datamanager.save_send_confirmation')
    save_send_confirmation_mock.side_effect = IntegrityError
    is_participant_mock = mocker.patch('src.dal.datamanager.is_participant')
    is_participant_mock.return_value = True

    answer = confirmationshandler.handle_message_content(user, message)

    assert answer == expected_answer


@pytest.mark.parametrize('message', [
    'wyslano',
    'wysłano',
])
def test_when_there_is_error_on_saving_sent_confirmation_should_return_error_text(message, mocker):
    user = 'someuser'
    expected_answer = [(user, strings.error_text)]
    save_send_confirmation_mock = mocker.patch('src.dal.datamanager.save_send_confirmation')
    save_send_confirmation_mock.side_effect = Exception
    is_participant_mock = mocker.patch('src.dal.datamanager.is_participant')
    is_participant_mock.return_value = True

    answer = confirmationshandler.handle_message_content(user, message)

    assert answer == expected_answer


@pytest.mark.freeze_time('2012-01-14 12:12')
def test_when_message_has_sent_command_with_valid_tracking_url_should_save_confirmation_with_url(mocker):
    url = 'http://www.paczkowisko.com.pl/tracking/9308490i9ACB333'
    message = f'wyslano {url}'
    user = 'someuser'
    expected_datetime = datetime.datetime(2012, 1, 14, 12, 12)

    is_participant_mock = mocker.patch('src.dal.datamanager.is_participant')
    is_participant_mock.return_value = True
    mocker.patch('src.dal.datamanager.get_gift_receiver_from')

    save_send_confirmation_mock = mocker.patch('src.dal.datamanager.save_send_confirmation')

    confirmationshandler.handle_message_content(user, message)

    save_send_confirmation_mock.assert_called_once_with(user, expected_datetime, url)


@pytest.mark.freeze_time('2012-01-14 12:12')
def test_when_message_has_sent_command_with_invalid_url_should_save_only_confirmation_entry(mocker):
    message = f'wyslano blablabla'
    user = 'someuser'
    expected_datetime = datetime.datetime(2012, 1, 14, 12, 12)

    is_participant_mock = mocker.patch('src.dal.datamanager.is_participant')
    is_participant_mock.return_value = True
    mocker.patch('src.dal.datamanager.get_gift_receiver_from')

    save_send_confirmation_mock = mocker.patch('src.dal.datamanager.save_send_confirmation')

    confirmationshandler.handle_message_content(user, message)

    save_send_confirmation_mock.assert_called_once_with(user, expected_datetime, None)


def test_when_successfully_saved_sent_confirmation_with_valid_tracking_url_should_also_send_it_to_the_receiver(mocker):
    url = 'http://www.paczkowisko.com.pl/tracking/9308490i9ACB333'
    message = f'wyslano {url}'
    user = 'someuser'
    gift_receiver = 'gift_receiver'
    expected_answer = [
        (user, strings.sent_confirmation_saved),
        (gift_receiver, strings.package_sent_notification),
        (gift_receiver, f"{strings.tracking_url_text}: {url}")
    ]
    is_participant_mock = mocker.patch('src.dal.datamanager.is_participant')
    is_participant_mock.return_value = True
    mocker.patch('src.dal.datamanager.save_send_confirmation')
    gift_receiver_from_mock = mocker.patch('src.dal.datamanager.get_gift_receiver_from')
    gift_receiver_from_mock.return_value = gift_receiver

    answer = confirmationshandler.handle_message_content(user, message)

    assert answer == expected_answer


def test_confirmation_entry_has_invalid_url_should_not_send_it_to_the_receiver(mocker):
    message = f'wyslano cośtamcoś aaaa!'
    user = 'someuser'
    gift_receiver = 'gift_receiver'
    expected_answer = [
        (user, strings.sent_confirmation_saved),
        (gift_receiver, strings.package_sent_notification),
    ]
    is_participant_mock = mocker.patch('src.dal.datamanager.is_participant')
    is_participant_mock.return_value = True
    mocker.patch('src.dal.datamanager.save_send_confirmation')
    gift_receiver_from_mock = mocker.patch('src.dal.datamanager.get_gift_receiver_from')
    gift_receiver_from_mock.return_value = gift_receiver

    answer = confirmationshandler.handle_message_content(user, message)

    assert answer == expected_answer


@pytest.mark.freeze_time('2012-01-14 12:12')
def test_when_message_has_received_command_should_save_received_confirmation(mocker):
    user = 'someuser'
    message = 'otrzymano'
    expected_datetime = datetime.datetime(2012, 1, 14, 12, 12)
    is_participant_mock = mocker.patch('src.dal.datamanager.is_participant')
    is_participant_mock.return_value = True
    mocker.patch('src.dal.datamanager.get_gift_sender_for')
    mocker.patch('src.dal.datamanager.has_send_confirmation')
    save_received_confirmation_mock = mocker.patch('src.dal.datamanager.save_received_confirmation')

    confirmationshandler.handle_message_content(user, message)

    save_received_confirmation_mock.assert_called_once_with(user, expected_datetime)


def test_when_successfully_saved_received_confirmation_should_return_confirmation_text_and_notification(mocker):
    user = 'someuser'
    gift_sender = 'gift_sender'
    message = 'otrzymano'
    is_participant_mock = mocker.patch('src.dal.datamanager.is_participant')
    is_participant_mock.return_value = True
    mocker.patch('src.dal.datamanager.has_send_confirmation')
    get_gift_sender_for_mock = mocker.patch('src.dal.datamanager.get_gift_sender_for')
    get_gift_sender_for_mock.return_value = gift_sender
    expected_answer = [
        (user, strings.received_confirmation_saved),
        (gift_sender, strings.package_received_notificaton)
    ]
    mocker.patch('src.dal.datamanager.save_received_confirmation')

    answer = confirmationshandler.handle_message_content(user, message)

    assert answer == expected_answer


def test_when_saving_duplicated_received_confirmation_should_return_confirmation_already_exists_text(mocker):
    user = 'someuser'
    message = 'otrzymano'
    expected_answer = [(user, strings.confirmation_already_exists)]
    save_received_confirmation_mock = mocker.patch('src.dal.datamanager.save_received_confirmation')
    save_received_confirmation_mock.side_effect = IntegrityError
    is_participant_mock = mocker.patch('src.dal.datamanager.is_participant')
    is_participant_mock.return_value = True

    answer = confirmationshandler.handle_message_content(user, message)

    assert answer == expected_answer


def test_when_there_is_error_on_saving_received_confirmation_should_return_error_text(mocker):
    user = 'someuser'
    message = 'otrzymano'
    expected_answer = [(user, strings.error_text)]
    save_received_confirmation_mock = mocker.patch('src.dal.datamanager.save_received_confirmation')
    save_received_confirmation_mock.side_effect = Exception
    is_participant_mock = mocker.patch('src.dal.datamanager.is_participant')
    is_participant_mock.return_value = True

    answer = confirmationshandler.handle_message_content(user, message)

    assert answer == expected_answer


@pytest.mark.parametrize('message', [
    'wyslano',
    'wysłano',
])
def test_when_got_confirmation_from_user_not_in_participants_list_should_return_not_a_participant_text(message, mocker):
    user = 'someuser'
    expected_answer = [(user, strings.not_a_participant)]
    is_participant_mock = mocker.patch('src.dal.datamanager.is_participant')
    is_participant_mock.return_value = False

    answer = confirmationshandler.handle_message_content(user, message)

    assert answer == expected_answer


@pytest.mark.parametrize('message', [
    'Wyslano',
    'wysłano',
    'Wyslano',
    'wysłaNO',
    'wyslano:',
    'nadano',
])
def test_when_send_command_synonym_was_provided_should_also_recognize_it(message, mocker):
    user = 'someuser'
    save_send_confirmation_mock = mocker.patch('src.dal.datamanager.save_send_confirmation')
    is_participant_mock = mocker.patch('src.dal.datamanager.is_participant')
    is_participant_mock.return_value = True
    mocker.patch('src.dal.datamanager.get_gift_receiver_from')

    confirmationshandler.handle_message_content(user, message)

    save_send_confirmation_mock.assert_called_once()


@pytest.mark.parametrize('message', [
    'otrzymano',
    'OTRZYMANO',
    'OtRzYMaNo',
    'otrzymano:',
    'odebrano',
    'odebrane',
    'otrzymałam',
    'otrzymałem',
    'otrzymalam',
    'otrzymalem',
])
def test_when_received_command_synonym_was_provided_should_also_recognize_it(message, mocker):
    user = 'someuser'
    save_received_confirmation_mock = mocker.patch('src.dal.datamanager.save_received_confirmation')
    is_participant_mock = mocker.patch('src.dal.datamanager.is_participant')
    is_participant_mock.return_value = True
    mocker.patch('src.dal.datamanager.get_gift_sender_for')
    mocker.patch('src.dal.datamanager.has_send_confirmation')

    confirmationshandler.handle_message_content(user, message)

    save_received_confirmation_mock.assert_called_once()
