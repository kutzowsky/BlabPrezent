#!/usr/bin/env python

import argparse
import logging
import os.path
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from config import settings
from dal import datamanager
from workers import XmppBot, WebsiteParsingBot, gift_assignment_draw, GiftAssignmentSender


def set_logger():
    global logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler('../bot.log')
    file_handler.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def create_db_if_not_exist():
    if not os.path.exists(settings.General.database_file):
        logger.info(f'Database file does not exist. Creating.')
        datamanager.create_db()


def action_bot():
    if settings.General.mode == 'www':
        bot = WebsiteParsingBot()
        bot.login(settings.WebsiteBot.login, settings.WebsiteBot.password)
        bot.try_create_latest_message_file()
        bot.start_listening()

        logger.info('WWW bot started')
    elif settings.General.mode == 'xmpp':
        bot = XmppBot(settings.JabberBot.jid, settings.JabberBot.password, settings.JabberBot.blabler_bot_jid)
        bot.connect()
        bot.process()

        logger.info('XMPP bot started')


def action_draw():
    gift_assignment_draw()


def action_send_assignments():
    sender = GiftAssignmentSender(mode=settings.General.mode)
    sender.send_assignments()


def run_action_from_arguments():
    parser = argparse.ArgumentParser(description='Blabprezent CLI')

    parser.add_argument(
        'mode',
        choices=['bot', 'draw', 'send-assignments'],
        help='Mode of operation'
    )

    args = parser.parse_args()

    logger.info(f'Selected mode: {args.mode}')

    if args.mode == 'bot':
        action_bot()
    elif args.mode == 'draw':
        action_draw()
    elif args.mode == 'send-assignments':
        action_send_assignments()


if __name__ == '__main__':
    set_logger()
    create_db_if_not_exist()
    run_action_from_arguments()
