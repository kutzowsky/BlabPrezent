from src.workers import giftdraw
from unittest.mock import call


def test_gift_assignment_draw_should_not_throw(mocker):
    random_choice_mock = mocker.patch('random.choice')
    random_choice_mock.side_effect = lambda x: x[0]
    mocker.patch('src.dal.datamanager.get_participants')

    giftdraw.gift_assignment_draw()


def test_gift_assignment_draw_should_save_gift_assignment_for_all_participants(mocker):
    participants = ['misia', 'bela', 'kasia', 'konfacela']
    random_choice_mock = mocker.patch('random.choice')
    random_choice_mock.side_effect = lambda x: x[0]
    get_participants_mock = mocker.patch('src.dal.datamanager.get_participants')
    get_participants_mock.return_value = participants
    save_gift_assignment_mock = mocker.patch('src.dal.datamanager.save_gift_assignment')

    giftdraw.gift_assignment_draw()

    save_gift_assignment_mock.assert_called()
    assert save_gift_assignment_mock.call_count == len(participants)


def test_gift_assignment_draw_should_(mocker):
    participants = ['misia', 'bela', 'kasia', 'konfacela']
    expected_calls = [
        call('misia', 'bela'),
        call('bela', 'misia'),
        call('kasia', 'konfacela'),
        call('konfacela', 'kasia')
    ]
    random_choice_mock = mocker.patch('random.choice')
    random_choice_mock.side_effect = lambda x: x[0]
    get_participants_mock = mocker.patch('src.dal.datamanager.get_participants')
    get_participants_mock.return_value = participants
    save_gift_assignment_mock = mocker.patch('src.dal.datamanager.save_gift_assignment')

    giftdraw.gift_assignment_draw()

    save_gift_assignment_mock.assert_has_calls(expected_calls, any_order=True)
