#!/usr/bin/env python

import random

from dal import datamanager

#todo otestowac jakos
all_participants = datamanager.get_participants()
participants_without_gift = list(all_participants)

for participant in all_participants:
    to_gift = participant

    while to_gift == participant:
        to_gift = random.choice(participants_without_gift)

    print(participant, '->', to_gift)
    datamanager.save_gift_assignment(participant, to_gift)
    participants_without_gift.remove(to_gift)