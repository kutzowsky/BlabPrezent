#!/usr/bin/env python

import random

from src.dal import datamanager


def gift_assignment_draw():
    all_participants = datamanager.get_participants()
    participants_without_gift = list(all_participants)

    for sender in all_participants:
        possible_receivers = [x for x in participants_without_gift if x != sender]
        receiver = random.choice(possible_receivers)

        print(sender, '->', receiver)
        datamanager.save_gift_assignment(sender, receiver)
        participants_without_gift.remove(receiver)
