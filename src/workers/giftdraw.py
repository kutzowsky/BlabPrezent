#!/usr/bin/env python

import random
import logging

from src.dal import datamanager

logger = logging.getLogger()


def gift_assignment_draw():
    logger.info('Gift draw started')
    all_participants = datamanager.get_all_participants()
    participants_without_gift = list(all_participants)

    for sender in all_participants:
        possible_receivers = [x for x in participants_without_gift if x != sender]
        receiver = random.choice(possible_receivers)

        logger.info(f'{sender} -> {receiver}')

        datamanager.save_gift_assignment(sender, receiver)
        participants_without_gift.remove(receiver)

    logger.info('Gift draw finished')
