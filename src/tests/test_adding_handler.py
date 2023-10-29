import pytest

from commandhandlers import addinghandler
from config import strings

def test_handle_message_content_should_not_throw():
    addinghandler.handle_message_content('user', 'content')


def test_when_message_has_no_add_command_should_return_help_text():
    user = 'someuser'
    expected_answer = [(user, strings.help_text)]
    answer = addinghandler.handle_message_content(user, 'nie dodawaj, odejmuj!')

    assert answer == expected_answer


def test_when_message_has_no_add_command_should_not_try_to_save_data(mocker):
    save_user_data_mock = mocker.patch('dal.datamanager.save_user_data')

    addinghandler.handle_message_content('user', 'nie dodawaj, odejmuj!')

    save_user_data_mock.assert_not_called()


def test_when_message_has_add_command_should_try_to_save_data(mocker):
    user = 'anna'
    address = 'Anna Maria Smutna 22-111 Ma twarz'
    message = f'dodaj {address}'
    save_user_data_mock = mocker.patch('dal.datamanager.save_user_data')

    addinghandler.handle_message_content(user, message)

    save_user_data_mock.assert_called_once_with(user, address)


def test_when_successfully_saved_user_data_should_return_data_saved_text(mocker):
    user = 'someuser'
    expected_answer = [(user, strings.data_saved)]
    mocker.patch('dal.datamanager.save_user_data')

    answer = addinghandler.handle_message_content(user, 'dodaj mnie!')

    assert answer == expected_answer


def test_when_there_is_error_with_saving_user_data_should_return_error_text(mocker):
    user = 'someuser'
    expected_answer = [(user, strings.error_text)]
    save_user_data_mock = mocker.patch('dal.datamanager.save_user_data')
    save_user_data_mock.side_effect = Exception

    answer = addinghandler.handle_message_content(user, 'dodaj mnie!')

    assert answer == expected_answer


@pytest.mark.parametrize('message', [
    'DODAJ',
    'DoDaj',
    'dodaj',
    'Dodaj',
])
def test_when_command_has_different_letter_case_should_also_recognize_it(message, mocker):
    user = 'someuser'
    save_user_data_mock = mocker.patch('dal.datamanager.save_user_data')

    addinghandler.handle_message_content(user, message)

    save_user_data_mock.assert_called_once()
