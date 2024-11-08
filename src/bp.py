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


def action_status_users():
    user_data = datamanager.get_all_addresses()
    print(f'Uczestników: {len(user_data)}')
    for user_entry in user_data:
        print(f'{user_entry[0]: <13}{user_entry[1]}')


def action_status_gifts():
    packages = datamanager.get_all_not_sent_packages()
    print(f'Niewysłane: {len(packages)}')
    for package in packages:
        print(f'{package[0]}->{package[1]}')
    print()

    packages = datamanager.get_all_sent_packages()
    print(f'W drodze: {len(packages)}')
    for package in packages:
        print(f'{package[0]}->{package[1]: <13}{package[2]} {package[3] or ''}')
    print()

    packages = datamanager.get_all_received_packages()
    print(f'Odebrane: {len(packages)}')
    for package in packages:
        print(f'{package[0]}->{package[1]: <13}{package[2]} {package[3]} {package[4] or ''}')


def create_parser():
    parser = argparse.ArgumentParser(description='Blabprezent CLI')
    subparsers = parser.add_subparsers(dest='mode', help='Available modes')
    subparsers.add_parser('bot', help='Start bot')
    subparsers.add_parser('draw', help='Gift draw')
    subparsers.add_parser('send-assignments', help='Send gift assignments')
    status_parser = subparsers.add_parser('status', help='Check status')
    status_subparsers = status_parser.add_subparsers(dest='status_type', help='Status type')
    status_subparsers.add_parser('users', help='Check participant list')
    status_subparsers.add_parser('gifts', help='Check gift status')
    return parser, status_parser


def run_action_from_arguments():
    parser, status_parser = create_parser()

    args = parser.parse_args()

    logger.info(f'Selected mode: {args.mode}')

    if args.mode == 'bot':
        action_bot()
    elif args.mode == 'draw':
        action_draw()
    elif args.mode == 'send-assignments':
        action_send_assignments()
    elif args.mode == 'status':
        if args.status_type == 'users':
            action_status_users()
        elif args.status_type == 'gifts':
            action_status_gifts()
        else:
            status_parser.print_help()
    else:
        parser.print_help()


if __name__ == '__main__':
    set_logger()
    create_db_if_not_exist()
    run_action_from_arguments()
