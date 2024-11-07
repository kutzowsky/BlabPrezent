import pytest

from src.commandhandlers import userdatahandler
from src.config import strings


def test_handle_message_content_should_not_throw():
    userdatahandler.handle_message_content('user', 'content')


def test_when_message_has_unknown_command_should_return_help_text():
    user = 'someuser'
    expected_answer = [(user, strings.help_text)]
    answer = userdatahandler.handle_message_content(user, 'nie dodawaj, odejmuj!')

    assert answer == expected_answer


def test_when_message_has_unknown_command_should_not_try_to_save_data(mocker):
    save_user_data_mock = mocker.patch('src.dal.datamanager.save_user_data')

    userdatahandler.handle_message_content('user', 'nie dodawaj, odejmuj!')

    save_user_data_mock.assert_not_called()


def test_when_message_has_add_command_should_try_to_save_data(mocker):
    user = 'anna'
    address = 'Anna Maria Smutna 22-111 Ma twarz'
    message = f'dodaj {address}'
    save_user_data_mock = mocker.patch('src.dal.datamanager.save_user_data')

    userdatahandler.handle_message_content(user, message)

    save_user_data_mock.assert_called_once_with(user, address)


def test_when_successfully_saved_user_data_should_return_data_saved_text(mocker):
    user = 'someuser'
    expected_answer = [(user, strings.data_saved)]
    mocker.patch('src.dal.datamanager.save_user_data')

    answer = userdatahandler.handle_message_content(user, 'dodaj mnie!')

    assert answer == expected_answer


def test_when_there_is_error_with_saving_user_data_should_return_error_text(mocker):
    user = 'someuser'
    expected_answer = [(user, strings.error_text)]
    save_user_data_mock = mocker.patch('src.dal.datamanager.save_user_data')
    save_user_data_mock.side_effect = Exception

    answer = userdatahandler.handle_message_content(user, 'dodaj mnie!')

    assert answer == expected_answer


@pytest.mark.parametrize('message', [
    'DODAJ',
    'DoDaj',
    'dodaj',
    'Dodaj',
    'dodaj:'
])
def test_when_command_synonym_was_provided_should_also_recognize_it(message, mocker):
    user = 'someuser'
    save_user_data_mock = mocker.patch('src.dal.datamanager.save_user_data')

    userdatahandler.handle_message_content(user, message)

    save_user_data_mock.assert_called_once()


def test_when_message_has_delete_command_should_try_to_delete_user_data(mocker):
    user = 'maruda'
    message = 'usuń'
    delete_user_data_mock = mocker.patch('src.dal.datamanager.delete_user_data')
    is_participant_mock = mocker.patch('src.dal.datamanager.is_participant')
    is_participant_mock.return_value = True

    userdatahandler.handle_message_content(user, message)

    delete_user_data_mock.assert_called_once_with(user)


def test_when_successfully_deleted_user_data_should_return_data_deleted_text(mocker):
    user = 'maruda'
    message = 'usuń'
    expected_answer = [('maruda', strings.data_deleted)]
    mocker.patch('src.dal.datamanager.delete_user_data')
    is_participant_mock = mocker.patch('src.dal.datamanager.is_participant')
    is_participant_mock.return_value = True

    answer = userdatahandler.handle_message_content(user, message)

    assert answer == expected_answer


def test_when_there_is_error_with_deleting_user_data_should_return_error_text(mocker):
    user = 'maruda'
    message = 'usuń'
    expected_answer = [(user, strings.error_text)]
    delete_user_data_mock = mocker.patch('src.dal.datamanager.delete_user_data')
    delete_user_data_mock.side_effect = Exception
    is_participant_mock = mocker.patch('src.dal.datamanager.is_participant')
    is_participant_mock.return_value = True

    answer = userdatahandler.handle_message_content(user, message)

    assert answer == expected_answer


def test_when_unknown_user_sends_delete_command_should_not_try_to_delete_data_and_send_not_a_participant_text(mocker):
    user = 'maruda'
    message = 'usuń'
    expected_answer = [('maruda', strings.not_a_participant)]
    delete_user_data_mock = mocker.patch('src.dal.datamanager.delete_user_data')
    is_participant_mock = mocker.patch('src.dal.datamanager.is_participant')
    is_participant_mock.return_value = False

    answer = userdatahandler.handle_message_content(user, message)

    assert answer == expected_answer
    delete_user_data_mock.assert_not_called()
